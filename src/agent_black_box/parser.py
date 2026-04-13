from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_black_box.models import TraceEvent, TraceRun


DEFAULT_RUN_ID = "unknown-run"


def parse_jsonl_trace(path: str | Path) -> TraceRun:
    path = Path(path)
    run = TraceRun(run_id=DEFAULT_RUN_ID)

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue

        obj = json.loads(line)
        _ingest_event(run, obj)

    return run


def _ingest_event(run: TraceRun, obj: dict[str, Any]) -> None:
    run.run_id = str(obj.get("run_id") or run.run_id)
    run.agent = obj.get("agent") or run.agent
    run.session_id = obj.get("session_id") or run.session_id

    event = TraceEvent(
        ts=str(obj.get("ts") or obj.get("timestamp") or "unknown-ts"),
        kind=str(obj.get("kind") or obj.get("type") or "unknown"),
        source=str(obj.get("source") or "unknown"),
        data={k: v for k, v in obj.items() if k not in {"run_id", "agent", "session_id", "ts", "timestamp", "kind", "type", "source"}},
    )
    run.add_event(event)
