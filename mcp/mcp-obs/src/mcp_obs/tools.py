"""Tool schemas, handlers, and registry for the observability MCP server."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from mcp.types import Tool
from pydantic import BaseModel, Field

from mcp_obs.client import ObsClient


ToolPayload = dict[str, Any]
ToolHandler = Callable[[ObsClient, BaseModel], Awaitable[ToolPayload]]


class LogsSearchArgs(BaseModel):
    query: str = Field(
        description=(
            "LogsQL query string, for example: _time:10m service.name:\"Learning Management Service\" severity:ERROR"
        )
    )
    limit: int = Field(default=50, ge=1, le=500, description="Maximum number of records.")


class LogsErrorCountArgs(BaseModel):
    minutes: int = Field(default=10, ge=1, le=1440, description="Time window in minutes.")
    service_name: str | None = Field(
        default="Learning Management Service",
        description="Optional service.name filter.",
    )


class TracesListArgs(BaseModel):
    service: str = Field(
        default="Learning Management Service",
        description="Jaeger service name to query recent traces for.",
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return.")


class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID returned by logs/traces query.")


@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        schema.pop("$defs", None)
        schema.pop("title", None)
        return Tool(name=self.name, description=self.description, inputSchema=schema)


async def _logs_search(client: ObsClient, args: BaseModel) -> ToolPayload:
    if not isinstance(args, LogsSearchArgs):
        raise TypeError(f"Expected LogsSearchArgs, got {type(args).__name__}")
    return await client.logs_search(query=args.query, limit=args.limit)


async def _logs_error_count(client: ObsClient, args: BaseModel) -> ToolPayload:
    if not isinstance(args, LogsErrorCountArgs):
        raise TypeError(f"Expected LogsErrorCountArgs, got {type(args).__name__}")
    return await client.logs_error_count(minutes=args.minutes, service_name=args.service_name)


async def _traces_list(client: ObsClient, args: BaseModel) -> ToolPayload:
    if not isinstance(args, TracesListArgs):
        raise TypeError(f"Expected TracesListArgs, got {type(args).__name__}")
    return await client.traces_list(service=args.service, limit=args.limit)


async def _traces_get(client: ObsClient, args: BaseModel) -> ToolPayload:
    if not isinstance(args, TracesGetArgs):
        raise TypeError(f"Expected TracesGetArgs, got {type(args).__name__}")
    return await client.traces_get(trace_id=args.trace_id)


TOOL_SPECS = (
    ToolSpec(
        "logs_search",
        "Search structured logs in VictoriaLogs with a LogsQL query.",
        LogsSearchArgs,
        _logs_search,
    ),
    ToolSpec(
        "logs_error_count",
        "Count recent error logs grouped by service.",
        LogsErrorCountArgs,
        _logs_error_count,
    ),
    ToolSpec(
        "traces_list",
        "List recent traces for a service from VictoriaTraces.",
        TracesListArgs,
        _traces_list,
    ),
    ToolSpec(
        "traces_get",
        "Fetch full trace details by trace ID from VictoriaTraces.",
        TracesGetArgs,
        _traces_get,
    ),
)

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
