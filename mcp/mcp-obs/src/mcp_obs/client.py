"""Async clients for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

import httpx


class ObsClient:
    def __init__(self, victorialogs_url: str, victoriatraces_url: str) -> None:
        self._logs_base = victorialogs_url.rstrip("/")
        self._traces_base = victoriatraces_url.rstrip("/")
        self._http = httpx.AsyncClient(timeout=httpx.Timeout(20.0, connect=10.0))

    async def __aenter__(self) -> "ObsClient":
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def logs_search(self, *, query: str, limit: int = 50) -> dict[str, Any]:
        url = f"{self._logs_base}/select/logsql/query"
        response = await self._http.get(url, params={"query": query, "limit": limit})
        response.raise_for_status()

        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        parsed: list[dict[str, Any]] = []
        for line in lines:
            try:
                value = json.loads(line)
                if isinstance(value, dict):
                    parsed.append(value)
            except json.JSONDecodeError:
                continue

        return {
            "query": query,
            "limit": limit,
            "returned": len(parsed),
            "logs": parsed,
        }

    async def logs_error_count(
        self,
        *,
        minutes: int = 10,
        service_name: str | None = None,
    ) -> dict[str, Any]:
        filters = [f"_time:{minutes}m", "severity:ERROR"]
        if service_name:
            filters.append(f'service.name:"{service_name}"')
        query = " ".join(filters)
        result = await self.logs_search(query=query, limit=200)

        per_service: Counter[str] = Counter()
        for item in result["logs"]:
            service = (
                str(item.get("service.name") or item.get("resource.service.name") or "unknown")
                .strip()
            )
            per_service[service] += 1

        return {
            "query": query,
            "window_minutes": minutes,
            "total_errors": sum(per_service.values()),
            "errors_per_service": dict(per_service),
        }

    async def traces_list(self, *, service: str, limit: int = 10) -> dict[str, Any]:
        url = f"{self._traces_base}/select/jaeger/api/traces"
        response = await self._http.get(url, params={"service": service, "limit": limit})
        response.raise_for_status()
        payload = response.json()

        traces = payload.get("data", []) if isinstance(payload, dict) else []
        return {
            "service": service,
            "limit": limit,
            "returned": len(traces),
            "traces": traces,
        }

    async def traces_get(self, *, trace_id: str) -> dict[str, Any]:
        url = f"{self._traces_base}/select/jaeger/api/traces/{trace_id}"
        response = await self._http.get(url)
        response.raise_for_status()
        payload = response.json()

        traces = payload.get("data", []) if isinstance(payload, dict) else []
        return {
            "trace_id": trace_id,
            "returned": len(traces),
            "trace": traces[0] if traces else None,
        }
