from __future__ import annotations

from collections import Counter
from typing import Any

from agent_black_box.models import TraceRun
from agent_black_box.timeline import _render_value


PREFERRED_DIFF_KEYS = ["tool", "tool_call_id", "arguments", "command", "path", "status", "is_error", "message", "content", "details", "name"]
COMPACT_SKIP_EVENT_KINDS = {"assistant_thinking", "session_start", "model_change", "thinking_level_change", "model-snapshot"}
COMPACT_IGNORE_DATA_KEYS = {"tool_call_id", "message_id", "parent_id", "id", "parentId", "responseId", "timestamp"}
IMPORTANT_FOCUS_KINDS = {"prompt", "tool_call", "tool_result", "assistant_message", "failure", "warning", "command", "completion"}


def diff_runs(left: TraceRun, right: TraceRun, compact: bool = False, focus: bool = False) -> str:
    left_events = [event for event in left.events if not compact or event.kind not in COMPACT_SKIP_EVENT_KINDS]
    right_events = [event for event in right.events if not compact or event.kind not in COMPACT_SKIP_EVENT_KINDS]

    if focus:
        return _render_focused_diff(left, right, left_events, right_events, compact=compact)

    left_label = f"{len(left_events)} shown / {left.event_count} total" if compact else f"{left.event_count} events"
    right_label = f"{len(right_events)} shown / {right.event_count} total" if compact else f"{right.event_count} events"
    lines = [
        "Run Diff",
        "--------",
        f"left:  {left.run_id} ({left_label})",
        f"right: {right.run_id} ({right_label})",
        "",
    ]

    max_len = max(len(left_events), len(right_events))
    differences = 0
    first_divergence = None
    event_word = "shown event" if compact else "event"

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
        f"summary: {differences} difference(s)",
        f"first divergence: {event_word} {first_divergence}",
        "",
    ]

    return "\n".join(lines[:4] + summary + lines[4:]).rstrip()


def _render_focused_diff(left: TraceRun, right: TraceRun, left_events, right_events, compact: bool) -> str:
    left_prompt = next((event for event in left_events if event.kind == "prompt"), None)
    right_prompt = next((event for event in right_events if event.kind == "prompt"), None)
    left_tools = Counter(event.data.get("tool") for event in left_events if event.kind == "tool_call" and event.data.get("tool"))
    right_tools = Counter(event.data.get("tool") for event in right_events if event.kind == "tool_call" and event.data.get("tool"))
    left_focus = [event for event in left_events if event.kind in IMPORTANT_FOCUS_KINDS]
    right_focus = [event for event in right_events if event.kind in IMPORTANT_FOCUS_KINDS]

    lines = [
        "Focused Diff",
        "============",
        "",
        f"left:  {left.run_id}",
        f"right: {right.run_id}",
        "",
        "Overview",
        "--------",
        f"left shown events:  {len(left_events)}",
        f"right shown events: {len(right_events)}",
        f"prompt match: {'yes' if _normalized_prompt_text(left_prompt) == _normalized_prompt_text(right_prompt) else 'no'}",
    ]

    shared_tools = sorted(set(left_tools) & set(right_tools))
    left_only_tools = sorted(set(left_tools) - set(right_tools))
    right_only_tools = sorted(set(right_tools) - set(left_tools))
    lines.append(f"shared tools: {', '.join(shared_tools) if shared_tools else 'none'}")
    if left_only_tools:
        lines.append(f"left-only tools: {', '.join(left_only_tools)}")
    if right_only_tools:
        lines.append(f"right-only tools: {', '.join(right_only_tools)}")

    lines.extend(["", "Key Differences", "---------------"])
    for bullet in _focused_bullets(left_events, right_events):
        lines.append(f"- {bullet}")

    lines.extend(["", "Preview", "-------"])
    for label, events in [("left", left_focus[:5]), ("right", right_focus[:5])]:
        lines.append(f"{label}:")
        for event in events:
            lines.append(f"  - {_format_event(event, compact=compact)}")

    return "\n".join(lines).rstrip()


def _focused_bullets(left_events, right_events) -> list[str]:
    bullets: list[str] = []

    left_message_edit = any(event.kind == "tool_call" and event.data.get("tool") == "message" for event in left_events)
    right_message_edit = any(event.kind == "tool_call" and event.data.get("tool") == "message" for event in right_events)
    if left_message_edit and right_message_edit:
        bullets.append("both runs reach a Discord message edit step")
    elif left_message_edit or right_message_edit:
        bullets.append("only one run reaches a Discord message edit step")

    left_failures = [event for event in left_events if event.data.get("is_error") is True or event.kind == "failure"]
    right_failures = [event for event in right_events if event.data.get("is_error") is True or event.kind == "failure"]
    if right_failures and not left_failures:
        bullets.append("right run includes an error path that does not appear in the left run")
    elif left_failures and not right_failures:
        bullets.append("left run includes an error path that does not appear in the right run")

    if len(right_events) > len(left_events):
        bullets.append(f"right run explores more steps before completion ({len(right_events)} vs {len(left_events)})")
    elif len(left_events) > len(right_events):
        bullets.append(f"left run explores more steps before completion ({len(left_events)} vs {len(right_events)})")

    left_tools = Counter(event.data.get("tool") for event in left_events if event.kind == "tool_call" and event.data.get("tool"))
    right_tools = Counter(event.data.get("tool") for event in right_events if event.kind == "tool_call" and event.data.get("tool"))
    for tool in sorted(set(left_tools) | set(right_tools)):
        if left_tools[tool] != right_tools[tool]:
            bullets.append(f"tool usage differs for {tool} ({left_tools[tool]} vs {right_tools[tool]})")

    return bullets or ["no focused differences detected"]


def _prompt_text(event) -> str | None:
    if event is None:
        return None
    return event.data.get("message") or event.data.get("content")


def _normalized_prompt_text(event) -> str | None:
    text = _prompt_text(event)
    if text is None:
        return None
    lines = [line.rstrip() for line in str(text).splitlines() if not line.startswith("Current time:")]
    return "\n".join(lines).strip()


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
        if compact and key == "tool_call_id":
            continue
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
