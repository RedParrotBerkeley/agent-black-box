from __future__ import annotations

from agent_black_box.models import TraceRun


def diff_runs(left: TraceRun, right: TraceRun) -> str:
    lines = [
        "run diff",
        f"- left: {left.run_id} ({left.event_count} events)",
        f"- right: {right.run_id} ({right.event_count} events)",
        "",
    ]

    max_len = max(left.event_count, right.event_count)
    differences = 0
    first_divergence = None

    for idx in range(max_len):
        left_event = left.events[idx] if idx < left.event_count else None
        right_event = right.events[idx] if idx < right.event_count else None

        if _event_signature(left_event) == _event_signature(right_event):
            continue

        if first_divergence is None:
            first_divergence = idx + 1

        differences += 1
        label = _difference_label(left_event, right_event)
        lines.append(f"difference {differences} ({label}) at event {idx + 1}:")
        lines.append(f"  left : {_format_event(left_event)}")
        lines.append(f"  right: {_format_event(right_event)}")
        lines.append("")

    if differences == 0:
        lines.append("no event-level differences detected")
        return "\n".join(lines).rstrip()

    summary = [
        f"summary: {differences} difference(s) detected",
        f"first divergence: event {first_divergence}",
    ]

    return "\n".join(summary + [""] + lines).rstrip()


def _difference_label(left_event, right_event) -> str:
    if left_event is None and right_event is not None:
        return "added event"
    if left_event is not None and right_event is None:
        return "removed event"
    return "changed event"


def _event_signature(event) -> tuple | None:
    if event is None:
        return None
    return (event.ts, event.kind, event.source, tuple(sorted(event.data.items())))


def _format_event(event) -> str:
    if event is None:
        return "<missing>"

    detail = _format_data(event.data)
    if detail:
        return f"[{event.ts}] {event.kind} ({event.source}) | {detail}"
    return f"[{event.ts}] {event.kind} ({event.source})"


def _format_data(data: dict) -> str:
    if not data:
        return ""

    preferred_keys = ["message", "status", "tool", "command", "path", "name"]
    parts: list[str] = []

    for key in preferred_keys:
        value = data.get(key)
        if value is not None:
            parts.append(f"{key}={value}")

    if not parts:
        for key, value in sorted(data.items()):
            parts.append(f"{key}={value}")

    return ", ".join(parts)
