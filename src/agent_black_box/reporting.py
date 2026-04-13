from __future__ import annotations

from collections import Counter

from agent_black_box.models import TraceRun


IMPORTANT_KINDS = {"failure", "warning", "command", "tool_call", "tool_result", "file_write", "completion"}


def render_incident_summary(run: TraceRun) -> str:
    counts = Counter(event.kind for event in run.events)
    lines = [
        f"# Incident Summary: {run.run_id}",
        "",
        f"- agent: {run.agent or 'unknown'}",
        f"- session_id: {run.session_id or 'unknown'}",
        f"- total events: {run.event_count}",
        "",
        "## Event Counts",
    ]

    for kind, count in sorted(counts.items()):
        lines.append(f"- {kind}: {count}")

    lines.extend([
        "",
        "## Key Events",
    ])

    for event in run.events:
        if event.kind not in IMPORTANT_KINDS:
            continue
        lines.append(f"- [{event.ts}] {event.kind} ({event.source}) {_event_detail(event.data)}".rstrip())

    return "\n".join(lines)


def _event_detail(data: dict) -> str:
    if not data:
        return ""
    parts = []
    for key in ["message", "status", "tool", "command", "path", "name"]:
        value = data.get(key)
        if value is not None:
            parts.append(f"{key}={value}")
    if not parts:
        return str(data)
    return " | " + ", ".join(parts)
