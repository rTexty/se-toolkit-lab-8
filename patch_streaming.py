import sys
import os

target = "qwen-code-api/src/qwen_code_api/routes/chat.py"
with open(target, "r") as f:
    content = f.read()

old_code = r"""
async def _handle_streaming(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    request_id: str,
    start_time: float,
) -> StreamingResponse:
"""
new_code = r"""
async def _handle_streaming(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    request_id: str,
    start_time: float,
) -> StreamingResponse:
    print(f"DEBUG PAYLOAD STREAMING: {payload}", file=sys.stderr)
"""
content = content.replace(old_code.strip(), new_code.strip())

with open(target, "w") as f:
    f.write(content)
