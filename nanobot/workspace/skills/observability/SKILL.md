---
name: observability
description: Use observability MCP tools to investigate logs and traces
always: true
---

- Use logs first, traces second:
  - Start with obs_logs_error_count for a quick signal.
  - Then use obs_logs_search to inspect concrete error events.
  - If logs contain trace_id values, use obs_traces_get on the newest relevant trace.
- Prefer LMS-focused filtering when the question is about LMS/backend health.
- For scoped checks, use a narrow time window (for example last 10 minutes) to avoid stale incidents.
- Do not dump raw JSON unless explicitly requested.
- Summarize findings as:
  - what failed
  - when it failed
  - affected service(s)
  - most likely cause based on logs/traces
- If no errors are found, state that clearly and mention the checked time window.
