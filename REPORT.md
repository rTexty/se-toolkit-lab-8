# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->
Prompt: What is the agentic loop?
🐈 nanobot
The agentic loop (also called the agent loop or perception-action cycle) is the fundamental operational pattern that enables AI agents to act autonomously. It's a continuous cycle of:

1. Perceive - Gather information from the environment (user input, files, APIs, sensors, etc.)
2. Reason - Process the information, plan actions, and decide what to do next
3. Act - Execute actions (call tools, send messages, modify files, make API calls, etc.)
4. Observe - See the results of actions and update the internal state
5. Repeat - Continue the cycle until the goal is achieved

Prompt: What labs are available in our LMS?
🐈 nanobot
Here are the available labs in your LMS:

1. Lab 01 - Products, Architecture & Roles
2. Lab 02 - Run, Fix, and Deploy a Backend Service
3. Lab 03 - Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 - Testing, Front-end, and AI Agents
5. Lab 05 - Data Pipeline and Analytics Dashboard
6. Lab 06 - Build Your Own Agent
7. Lab 07 - Build a Client with an AI Coding Agent
8. Lab 08 - lab-08

Would you like to see details about any specific lab, such as pass rates, completion rates, or top learners?
## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->
🐈 nanobot
Here are the available labs:

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 Lab 08 — lab-08

Is there a specific lab you'd like to know more about? I can help you with pass rates, completion rates, top learners, or other statistics for any of these labs.

🐈 nanobot
Yes, the LMS backend is healthy and currently has 56 items in the system.


## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->
🐈 nanobot
I can show you scores for any of the available labs. Which lab would you like to see scores for?

 1 Lab 01 – Products, Architecture & Roles
 2 Lab 02 — Run, Fix, and Deploy a Backend Service
 3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4 Lab 04 — Testing, Front-end, and AI Agents
 5 Lab 05 — Data Pipeline and Analytics Dashboard
 6 Lab 06 — Build Your Own Agent
 7 Lab 07 — Build a Client with an AI Coding Agent
 8 Lab 08 — lab-08

Or would you like me to show pass rates for all labs?

## Task 2A — Deployed agent

Startup logs (`docker compose --env-file .env.docker.secret logs nanobot --tail 200`):

nanobot-1  | Using config: /app/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-04-01 17:26:21.028 | INFO     | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-04-01 17:26:24.825 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-04-01 17:26:26.442 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'webchat': connected, 1 tools registered
nanobot-1  | 2026-04-01 17:26:26.442 | INFO     | nanobot.agent.loop:run:280 - Agent loop started
## Task 2B — Web client

Flutter + WebSocket checkpoint evidence:

1) Flutter is served via Caddy:
- `curl -sSI http://127.0.0.1:42002/flutter/ | head -n 1` -> `HTTP/1.1 200 OK`
- `curl -sI http://127.0.0.1:42002/flutter/main.dart.js | head -n 1` -> `HTTP/1.1 200 OK`

2) WebSocket `/ws/chat` accepts access key and returns agent response:

Request (via websocket):
{"content": "What labs are available?"}

Response:
{"type":"text","content":"Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n3. **Lab 03** — Backend API: Explore, Debug, Implement, Deploy\n4. **Lab 04** — Testing, Front-end, and AI Agents\n5. **Lab 05** — Data Pipeline and Analytics Dashboard\n6. **Lab 06** — Build Your Own Agent\n7. **Lab 07** — Build a Client with an AI Coding Agent\n8. **Lab 08** — lab-08\n\nWhich lab would you like to explore? I can show you pass rates, completion rates, top learners, group performance, or submission timelines for any of these.","format":"markdown"}

3) Corresponding nanobot logs confirm the full chain with no LLM error:
- `Processing message from webchat:...: What labs are available?`
- `HTTP Request: POST https://openrouter.ai/api/v1/chat/completions "HTTP/1.1 200 OK"`
- `Tool call: mcp_lms_lms_labs({})`
- `HTTP Request: GET http://backend:8000/items/ "HTTP/1.1 200 OK"`
## Task 3A — Structured logging

Structured logging evidence (VictoriaLogs + docker logs):

Happy-path excerpt (status 200, request_started -> request_completed):
{"_msg":"request_started","event":"request_started","method":"GET","path":"/items/","service.name":"Learning Management Service","severity":"INFO","trace_id":"538ee01575b78782690fa1933b0697d5"}
{"_msg":"auth_success","event":"auth_success","service.name":"Learning Management Service","severity":"INFO","trace_id":"538ee01575b78782690fa1933b0697d5"}
{"_msg":"db_query","event":"db_query","operation":"select","table":"item","service.name":"Learning Management Service","severity":"INFO","trace_id":"538ee01575b78782690fa1933b0697d5"}
{"_msg":"request_completed","event":"request_completed","status":"200","service.name":"Learning Management Service","severity":"INFO","trace_id":"538ee01575b78782690fa1933b0697d5"}

Error-path excerpt (postgres stopped, db_query error + status 500):
{"_msg":"request_started","event":"request_started","method":"GET","path":"/items/","service.name":"Learning Management Service","severity":"INFO","trace_id":"1cce3b86b31cfcb95530d68e191a0b25"}
{"_msg":"db_query","event":"db_query","operation":"select","table":"item","service.name":"Learning Management Service","severity":"ERROR","error":"[Errno -2] Name or service not known","trace_id":"1cce3b86b31cfcb95530d68e191a0b25"}
{"_msg":"items_list_failed","event":"items_list_failed","service.name":"Learning Management Service","severity":"ERROR","trace_id":"1cce3b86b31cfcb95530d68e191a0b25"}
{"_msg":"request_completed","event":"request_completed","status":"500","service.name":"Learning Management Service","severity":"ERROR","trace_id":"1cce3b86b31cfcb95530d68e191a0b25"}

VictoriaLogs query used:
_time:10m service.name:"Learning Management Service" severity:ERROR
## Task 3B — Traces

Trace evidence (VictoriaTraces Jaeger API):

Healthy trace (trace_id: 538ee01575b78782690fa1933b0697d5):
- serviceName: Learning Management Service
- spans include DB span: operationName="SELECT db-lab-8"
- HTTP span has http.status_code="200"

Excerpt:
{"traceID":"538ee01575b78782690fa1933b0697d5","operationName":"SELECT db-lab-8","processID":"p1"}
{"traceID":"538ee01575b78782690fa1933b0697d5","operationName":"GET /items/ http send","tags":[{"key":"http.status_code","value":"200"}]}

Error trace (trace_id: 1cce3b86b31cfcb95530d68e191a0b25):
- serviceName: Learning Management Service
- HTTP send span has http.status_code="500"
- error=true appears in span tags

Excerpt:
{"traceID":"1cce3b86b31cfcb95530d68e191a0b25","operationName":"GET /items/ http send","tags":[{"key":"http.status_code","value":"500"},{"key":"error","value":"true"}]}

VictoriaTraces endpoints used:
- /select/jaeger/api/traces?service=Learning Management Service&limit=3
- /select/jaeger/api/traces/<trace_id>
## Task 3C — Observability MCP tools

Observability MCP tools + agent responses:

Registered obs tools in nanobot logs:
- mcp_obs_logs_search
- mcp_obs_logs_error_count
- mcp_obs_traces_list
- mcp_obs_traces_get

Normal condition prompt:
Prompt: Any LMS backend errors in the last 10 minutes?
🐈 nanobot:
No LMS backend errors in the last 10 minutes. The Learning Management Service is running cleanly with zero errors detected.

Failure condition prompt (after stopping postgres and triggering LMS request):
Prompt: Any LMS backend errors in the last 10 minutes?
🐈 nanobot:
Yes, there are 6 errors in the Learning Management Service over the last 10 minutes. Let me search for the specific error details:

Related tool-call evidence from nanobot logs:
- Tool call: mcp_obs_logs_error_count({"minutes": 10, "service_name": "Learning Management Service"})
- HTTP GET http://victorialogs:9428/select/logsql/query?...severity:ERROR... -> 200 OK
## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
