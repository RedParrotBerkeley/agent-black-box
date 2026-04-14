from agent_black_box.adapters import parse_trace
from agent_black_box.diffing import diff_runs
from agent_black_box.parser import parse_jsonl_trace


def test_diff_runs_reports_changed_events(tmp_path):
    left_path = tmp_path / "left.jsonl"
    right_path = tmp_path / "right.jsonl"

    left_path.write_text(
        '{"run_id":"r1","ts":"1","kind":"command","source":"shell","command":"echo bad"}\n'
    )
    right_path.write_text(
        '{"run_id":"r2","ts":"1","kind":"command","source":"shell","command":"echo good"}\n'
    )

    left = parse_jsonl_trace(left_path)
    right = parse_jsonl_trace(right_path)
    rendered = diff_runs(left, right)

    assert "summary: 1 difference(s) detected" in rendered
    assert "first divergence: event 1" in rendered
    assert "difference 1 (changed event) at event 1:" in rendered
    assert "echo bad" in rendered
    assert "echo good" in rendered


def test_diff_runs_reports_added_event(tmp_path):
    left_path = tmp_path / "left.jsonl"
    right_path = tmp_path / "right.jsonl"

    left_path.write_text(
        '{"run_id":"r1","ts":"1","kind":"command","source":"shell","command":"echo one"}\n'
    )
    right_path.write_text(
        '{"run_id":"r2","ts":"1","kind":"command","source":"shell","command":"echo one"}\n'
        '{"run_id":"r2","ts":"2","kind":"completion","source":"assistant","message":"done"}\n'
    )

    left = parse_jsonl_trace(left_path)
    right = parse_jsonl_trace(right_path)
    rendered = diff_runs(left, right)

    assert "difference 1 (added event) at event 2:" in rendered
    assert "<missing>" in rendered
    assert "message=done" in rendered


def test_diff_runs_handles_openclaw_nested_tool_data(tmp_path):
    left_path = tmp_path / "left-openclaw.jsonl"
    right_path = tmp_path / "right-openclaw.jsonl"

    left_path.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-left","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"a1","parentId":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"tc1","name":"exec","arguments":{"command":"pytest -q"}}],"stopReason":"toolUse"}}',
            ]
        )
        + '\n'
    )
    right_path.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-right","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"a1","parentId":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"tc1","name":"exec","arguments":{"command":"python -m pytest -q"}}],"stopReason":"toolUse"}}',
            ]
        )
        + '\n'
    )

    left = parse_trace(left_path, source_format="openclaw-jsonl")
    right = parse_trace(right_path, source_format="openclaw-jsonl")
    rendered = diff_runs(left, right)

    assert "summary: 2 difference(s) detected" in rendered
    assert "tool=exec" in rendered
    assert "tool_call_id=tc1" in rendered


def test_diff_runs_compact_ignores_timestamp_only_changes(tmp_path):
    left_path = tmp_path / "left-openclaw.jsonl"
    right_path = tmp_path / "right-openclaw.jsonl"

    left_path.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-left","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"u1","timestamp":"2026-04-14T12:00:01Z","message":{"role":"user","content":[{"type":"text","text":"hello"}]}}',
            ]
        )
        + '\n'
    )
    right_path.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-right","timestamp":"2026-04-14T12:05:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"u9","timestamp":"2026-04-14T12:05:01Z","message":{"role":"user","content":[{"type":"text","text":"hello"}]}}',
            ]
        )
        + '\n'
    )

    left = parse_trace(left_path, source_format="openclaw-jsonl")
    right = parse_trace(right_path, source_format="openclaw-jsonl")
    full = diff_runs(left, right)
    compact = diff_runs(left, right, compact=True)

    assert "summary: 2 difference(s) detected" in full
    assert "no event-level differences detected" in compact
