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
