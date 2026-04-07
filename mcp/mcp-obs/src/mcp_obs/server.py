"""Stdio MCP server exposing observability tools for logs and traces."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from mcp_obs.client import ObsClient
from mcp_obs.settings import resolve_settings
from mcp_obs.tools import TOOL_SPECS, TOOLS_BY_NAME


def _text(data: dict[str, Any]) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False))]


def create_server(client: ObsClient) -> Server:
    server = Server("obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [spec.as_tool() for spec in TOOL_SPECS]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        spec = TOOLS_BY_NAME.get(name)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            args = spec.model.model_validate(arguments or {})
            return _text(await spec.handler(client, args))
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    settings = resolve_settings()
    async with ObsClient(
        victorialogs_url=settings.victorialogs_url,
        victoriatraces_url=settings.victoriatraces_url,
    ) as client:
        server = create_server(client)
        async with stdio_server() as (read_stream, write_stream):
            init_options = server.create_initialization_options()
            await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
