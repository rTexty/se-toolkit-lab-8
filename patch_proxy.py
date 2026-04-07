import sys
import os

target = "qwen-code-api/src/qwen_code_api/routes/chat.py"
with open(target, "r") as f:
    content = f.read()

# Replace the part in _handle_regular to print the payload
old_code = r"""
async def _handle_regular(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    request_id: str,
    start_time: float,
) -> JSONResponse:
    resp = await client.post(url, json=payload, headers=headers)
"""
new_code = r"""
async def _handle_regular(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    headers: dict[str, str],
    request_id: str,
    start_time: float,
) -> JSONResponse:
    print(f"DEBUG PAYLOAD TO OPENROUTER: {payload}", file=sys.stderr)
    resp = await client.post(url, json=payload, headers=headers)
"""
content = content.replace(old_code.strip(), new_code.strip())

with open(target, "w") as f:
    f.write(content)
