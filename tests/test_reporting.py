from agent_black_box.adapters import parse_trace
from agent_black_box.parser import parse_jsonl_trace
from agent_black_box.reporting import render_incident_summary


def test_render_incident_summary_smoke(tmp_path):
    trace = tmp_path / "trace.jsonl"
    trace.write_text(
        '{"run_id":"r1","agent":"demo","ts":"1","kind":"tool_result","source":"github","status":"failure","message":"bad"}\n'
        '{"run_id":"r1","agent":"demo","ts":"2","kind":"completion","source":"assistant","message":"done"}\n'
    )

    run = parse_jsonl_trace(trace)
    rendered = render_incident_summary(run)

    assert "Incident Summary: r1" in rendered
    assert "tool_result: 1" in rendered
    assert "completion: 1" in rendered
    assert "message=bad" in rendered


def test_render_incident_summary_openclaw_tool_result_details(tmp_path):
    trace = tmp_path / "openclaw-session.jsonl"
    trace.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-123","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"u1","parentId":"m1","timestamp":"2026-04-14T12:00:01Z","message":{"role":"user","content":[{"type":"text","text":"Fix the failing PR"}]}}',
                '{"type":"message","id":"a1","parentId":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"tc1","name":"exec","arguments":{"command":"pytest -q"}}],"stopReason":"toolUse"}}',
                '{"type":"message","id":"t1","parentId":"a1","timestamp":"2026-04-14T12:00:03Z","message":{"role":"toolResult","toolCallId":"tc1","toolName":"exec","content":[{"type":"text","text":"tests failed"}],"details":{"exitCode":1},"isError":true}}',
            ]
        )
        + '\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")
    rendered = render_incident_summary(run)

    assert "prompt: 1" in rendered
    assert "tool_call: 1" in rendered
    assert "tool_result: 1" in rendered
    assert "tool=exec" in rendered
    assert "tool_call_id=tc1" in rendered
    assert "is_error=True" in rendered
    assert "content=tests failed" in rendered


def test_render_incident_summary_compact_adds_compact_metadata(tmp_path):
    trace = tmp_path / "openclaw-session.jsonl"
    trace.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-123","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"th1","timestamp":"2026-04-14T12:00:01Z","message":{"role":"assistant","content":[{"type":"thinking","thinking":"long chain of thought"}]}}',
                '{"type":"message","id":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"user","content":[{"type":"text","text":"hello"}]}}',
            ]
        )
        + '\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")
    full = render_incident_summary(run)
    compact = render_incident_summary(run, compact=True)

    assert "key events:" not in full
    assert "filtered events:" not in full
    assert "filtered detail:" not in full
    assert "key events: 1" in compact
    assert "filtered events: 2" in compact
    assert "filtered detail: assistant_thinking=1, session_start=1" in compact
    assert "- assistant_thinking:" not in compact
    assert "- session_start:" not in compact
