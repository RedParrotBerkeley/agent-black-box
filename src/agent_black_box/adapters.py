from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_black_box.models import TraceEvent, TraceRun


def parse_trace(path: str | Path, source_format: str = "jsonl") -> TraceRun:
    if source_format == "jsonl":
        from agent_black_box.parser import parse_jsonl_trace

        return parse_jsonl_trace(path)

    if source_format == "openclaw-jsonl":
        return parse_openclaw_jsonl(path)

    raise ValueError(f"unsupported source format: {source_format}")


def parse_openclaw_jsonl(path: str | Path) -> TraceRun:
    path = Path(path)
    run = TraceRun(run_id="openclaw-run")

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        obj = json.loads(line)
        run.run_id = str(obj.get("run_id") or obj.get("session_id") or run.run_id)
        run.agent = obj.get("agent") or "openclaw"
        run.session_id = obj.get("session_id") or run.session_id
        run.add_event(
            TraceEvent(
                ts=str(obj.get("ts") or obj.get("timestamp") or "unknown-ts"),
                kind=str(obj.get("event") or obj.get("kind") or "unknown"),
                source=str(obj.get("source") or "openclaw"),
                data={k: v for k, v in obj.items() if k not in {"run_id", "agent", "session_id", "ts", "timestamp", "event", "kind", "source"}},
            )
        )

    return run
