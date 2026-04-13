from __future__ import annotations

from agent_black_box.models import TraceRun


REDACT_KEYS = {"api_key", "token", "authorization", "secret", "password"}


def redact_run(run: TraceRun) -> TraceRun:
    for event in run.events:
        for key in list(event.data.keys()):
            if key.lower() in REDACT_KEYS:
                event.data[key] = "[REDACTED]"
    return run
