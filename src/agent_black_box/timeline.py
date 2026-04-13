from __future__ import annotations

from agent_black_box.models import TraceRun


def render_timeline(run: TraceRun) -> str:
    lines = [
        f"run_id: {run.run_id}",
        f"agent: {run.agent or 'unknown'}",
        f"session_id: {run.session_id or 'unknown'}",
        f"events: {run.event_count}",
        "",
        "timeline:",
    ]

    for idx, event in enumerate(run.events, start=1):
        detail = _summarize_event_data(event.data)
        lines.append(f"{idx:02d}. [{event.ts}] {event.kind} ({event.source}) {detail}".rstrip())

    return "\n".join(lines)


def _summarize_event_data(data: dict) -> str:
    if not data:
        return ""

    preferred_keys = ["name", "tool", "command", "path", "status", "message"]
    parts: list[str] = []

    for key in preferred_keys:
        value = data.get(key)
        if value is not None:
            parts.append(f"{key}={value}")

    if not parts:
        first_key = next(iter(data.keys()))
        parts.append(f"{first_key}={data[first_key]}")

    return " | " + ", ".join(parts)
