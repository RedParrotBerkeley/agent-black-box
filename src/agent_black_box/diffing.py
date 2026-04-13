from __future__ import annotations

from agent_black_box.models import TraceRun


def diff_runs(left: TraceRun, right: TraceRun) -> str:
    lines = [
        f"left: {left.run_id} ({left.event_count} events)",
        f"right: {right.run_id} ({right.event_count} events)",
        "",
    ]

    max_len = max(left.event_count, right.event_count)
    differences = 0

    for idx in range(max_len):
        left_event = left.events[idx] if idx < left.event_count else None
        right_event = right.events[idx] if idx < right.event_count else None

        if _event_signature(left_event) == _event_signature(right_event):
            continue

        differences += 1
        lines.append(f"difference {differences}:")
        lines.append(f"  left : {_format_event(left_event)}")
        lines.append(f"  right: {_format_event(right_event)}")
        lines.append("")

    if differences == 0:
        lines.append("no event-level differences detected")

    return "\n".join(lines).rstrip()


def _event_signature(event) -> tuple | None:
    if event is None:
        return None
    return (event.ts, event.kind, event.source, tuple(sorted(event.data.items())))


def _format_event(event) -> str:
    if event is None:
        return "<missing>"
    if event.data:
        return f"[{event.ts}] {event.kind} ({event.source}) {event.data}"
    return f"[{event.ts}] {event.kind} ({event.source})"
