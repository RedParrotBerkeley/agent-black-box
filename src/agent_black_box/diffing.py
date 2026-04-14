from __future__ import annotations

from typing import Any

from agent_black_box.models import TraceRun
from agent_black_box.timeline import _render_value


PREFERRED_DIFF_KEYS = ["tool", "tool_call_id", "arguments", "command", "path", "status", "is_error", "message", "content", "details", "name"]
COMPACT_SKIP_EVENT_KINDS = {"assistant_thinking", "session_start", "model_change", "thinking_level_change", "model-snapshot"}
COMPACT_IGNORE_DATA_KEYS = {"tool_call_id", "message_id", "parent_id", "id", "parentId", "responseId", "timestamp"}


def diff_runs(left: TraceRun, right: TraceRun, compact: bool = False) -> str:
    left_events = [event for event in left.events if not compact or event.kind not in COMPACT_SKIP_EVENT_KINDS]
    right_events = [event for event in right.events if not compact or event.kind not in COMPACT_SKIP_EVENT_KINDS]
    left_label = f"{len(left_events)} visible events, {left.event_count} total" if compact else f"{left.event_count} events"
    right_label = f"{len(right_events)} visible events, {right.event_count} total" if compact else f"{right.event_count} events"
    lines = [
        "run diff",
        f"- left: {left.run_id} ({left_label})",
        f"- right: {right.run_id} ({right_label})",
        "",
    ]

    max_len = max(len(left_events), len(right_events))
    differences = 0
    first_divergence = None
    event_word = "visible event" if compact else "event"

    for idx in range(max_len):
        left_event = left_events[idx] if idx < len(left_events) else None
        right_event = right_events[idx] if idx < len(right_events) else None

        if _event_signature(left_event, compact=compact) == _event_signature(right_event, compact=compact):
            continue

        if first_divergence is None:
            first_divergence = idx + 1

        differences += 1
        label = _difference_label(left_event, right_event)
        lines.append(f"difference {differences} ({label}) at {event_word} {idx + 1}:")
        lines.append(f"  left : {_format_event(left_event, compact=compact)}")
        lines.append(f"  right: {_format_event(right_event, compact=compact)}")
        lines.append("")

    if differences == 0:
        lines.append("no event-level differences detected")
        return "\n".join(lines).rstrip()

    summary = [
        f"summary: {differences} difference(s) detected",
        f"first divergence: {event_word} {first_divergence}",
    ]

    return "\n".join(summary + [""] + lines).rstrip()


def _difference_label(left_event, right_event) -> str:
    if left_event is None and right_event is not None:
        return "added event"
    if left_event is not None and right_event is None:
        return "removed event"
    return "changed event"


def _event_signature(event, compact: bool = False) -> tuple | None:
    if event is None:
        return None
    return (event.kind, event.source, _normalize_data(event.data, compact=compact)) if compact else (event.ts, event.kind, event.source, _normalize_data(event.data, compact=compact))


def _normalize_data(data: dict[str, Any], compact: bool = False) -> tuple:
    normalized = []
    for key, value in sorted(data.items()):
        if compact and key in COMPACT_IGNORE_DATA_KEYS:
            continue
        normalized.append((key, _normalize_value(value, compact=compact)))
    return tuple(normalized)


def _normalize_value(value: Any, compact: bool = False):
    if isinstance(value, dict):
        return tuple((k, _normalize_value(v, compact=compact)) for k, v in sorted(value.items()) if not compact or k not in COMPACT_IGNORE_DATA_KEYS)
    if isinstance(value, list):
        return tuple(_normalize_value(v, compact=compact) for v in value)
    return value


def _format_event(event, compact: bool = False) -> str:
    if event is None:
        return "<missing>"

    detail = _format_data(event.kind, event.data, compact=compact)
    if detail:
        return f"[{event.ts}] {event.kind} ({event.source}) | {detail}"
    return f"[{event.ts}] {event.kind} ({event.source})"


def _format_data(kind: str, data: dict[str, Any], compact: bool = False) -> str:
    if not data:
        return ""

    parts: list[str] = []
    for key in PREFERRED_DIFF_KEYS:
        value = data.get(key)
        if value is not None and (not compact or key not in COMPACT_IGNORE_DATA_KEYS):
            parts.append(f"{key}={_render_value(kind, key, value, compact=compact)}")

    if parts:
        return ", ".join(parts)

    for key, value in sorted(data.items()):
        if compact and key in COMPACT_IGNORE_DATA_KEYS:
            continue
        parts.append(f"{key}={_render_value(kind, key, value, compact=compact)}")

    return ", ".join(parts)
