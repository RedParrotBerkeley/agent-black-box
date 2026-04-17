from agent_black_box.adapters import parse_trace
from agent_black_box.parser import parse_jsonl_trace
from agent_black_box.timeline import render_timeline


def test_render_timeline_smoke(tmp_path):
    trace = tmp_path / "trace.jsonl"
    trace.write_text(
        '{"run_id":"r1","agent":"demo","ts":"2026-04-13T00:00:00Z","kind":"prompt","source":"assistant","message":"hello"}\n'
        '{"run_id":"r1","agent":"demo","ts":"2026-04-13T00:00:01Z","kind":"command","source":"shell","command":"echo hi"}\n'
    )

    run = parse_jsonl_trace(trace)
    rendered = render_timeline(run)

    assert "run_id: r1" in rendered
    assert "prompt" in rendered
    assert "command" in rendered
    assert "echo hi" in rendered


def test_render_timeline_openclaw_tool_details(tmp_path):
    trace = tmp_path / "openclaw-session.jsonl"
    trace.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-123","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"message","id":"a1","parentId":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"tc1","name":"exec","arguments":{"command":"pytest -q"}}],"stopReason":"toolUse"}}',
                '{"type":"message","id":"t1","parentId":"a1","timestamp":"2026-04-14T12:00:03Z","message":{"role":"toolResult","toolCallId":"tc1","toolName":"exec","content":[{"type":"text","text":"tests failed"}],"details":{"exitCode":1},"isError":true}}',
            ]
        )
        + '\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")
    rendered = render_timeline(run)

    assert "tool_call" in rendered
    assert "tool=exec" in rendered
    assert "tool_call_id=tc1" in rendered
    assert "tool_result" in rendered
    assert "is_error=True" in rendered
    assert "content=tests failed" in rendered


def test_render_timeline_compact_omits_setup_and_thinking_events(tmp_path):
    trace = tmp_path / "openclaw-session.jsonl"
    trace.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-123","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"model_change","timestamp":"2026-04-14T12:00:00Z","model":"gpt-5.4"}',
                '{"type":"thinking_level_change","timestamp":"2026-04-14T12:00:00Z","thinking":"low"}',
                '{"type":"message","id":"th1","timestamp":"2026-04-14T12:00:01Z","message":{"role":"assistant","content":[{"type":"thinking","thinking":"long chain of thought"}]}}',
                '{"type":"message","id":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"user","content":[{"type":"text","text":"hello"}]}}',
            ]
        )
        + '\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")
    full = render_timeline(run)
    compact = render_timeline(run, compact=True)

    assert "session_start" in full
    assert "model_change" in full
    assert "thinking_level_change" in full
    assert "assistant_thinking" in full
    assert "visible_events:" not in full
    assert "01. [2026-04-14T12:00:00Z] session_start" not in compact
    assert "01. [2026-04-14T12:00:01Z] assistant_thinking" not in compact
    assert "events: 1 shown / 5 total" in compact
    assert "view: compact" in compact
    assert "filtered: 4 event(s) (assistant_thinking=1, model_change=1, session_start=1, thinking_level_change=1)" in compact
