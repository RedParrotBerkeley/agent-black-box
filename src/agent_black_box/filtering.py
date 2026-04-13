from __future__ import annotations

from agent_black_box.models import TraceRun


def filter_run(run: TraceRun, kinds: list[str] | None = None) -> TraceRun:
    if not kinds:
        return run

    allowed = {kind.strip() for kind in kinds if kind.strip()}
    run.events = [event for event in run.events if event.kind in allowed]
    return run
