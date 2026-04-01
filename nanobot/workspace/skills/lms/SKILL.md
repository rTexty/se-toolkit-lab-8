---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

- Which `lms_*` tools are available and when to use each one:
  - `lms_health`: Use to check backend connectivity status.
  - `lms_labs`: Use to fetch available lab options.
  - `lms_pass_rates`: Use to get pass rate statistics for labs.
  - `lms_learners`: Use to see details about the learners.
  - `lms_timeline`: Use to show progress timelines.
  - `lms_groups`: Use to get information on student groups.
  - `lms_top_learners`: Use to see best performers in labs.
  - `lms_completion_rate`: Use to see the percentage completion of labs.
  - `lms_sync_pipeline`: Use to monitor data syncing.
- When a lab parameter is needed and not provided, ask the user which lab they are referring to.
- When a lab choice is needed, call `lms_labs` first and provide good lab labels/values for the shared UI layer.
- Format numeric results nicely (percentages, counts). Include `%` for rates and format counts with commas.
- Keep responses concise and directly answer the question without unnecessary fluff.
- When the user asks "what can you do?", explain your current tools and limits clearly.
- If the user asks for scores, pass rates, completion, groups, timeline, or top learners without naming a lab, call `lms_labs` first to retrieve choices.
- If multiple labs are available, ask the user to choose one.
- Use each lab title as the default user-facing label unless the tool output gives a better identifier.
- Let the shared `structured-ui` skill decide how to present that choice on supported channels.
