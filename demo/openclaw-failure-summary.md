Incident Summary: sess-failure-demo
===============================

agent: openclaw
session: sess-failure-demo
events: 6
key events: 4
filtered events: 2
filtered detail: model_change=1, session_start=1

Event Counts
------------
- assistant_message: 1
- prompt: 1
- tool_call: 1
- tool_result: 1

Key Events
----------
- [2026-04-14T12:00:01Z] prompt (user)  | message=Fix the failing PR
- [2026-04-14T12:00:02Z] tool_call (assistant)  | tool=exec, arguments={command=pytest -q}
- [2026-04-14T12:00:03Z] tool_result (exec)  | tool=exec, is_error=True, content=tests failed, details={exitCode=1}
- [2026-04-14T12:00:04Z] assistant_message (assistant)  | message=Pytest failed on one assertion
