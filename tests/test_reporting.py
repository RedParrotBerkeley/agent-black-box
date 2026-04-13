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

    assert "# Incident Summary: r1" in rendered
    assert "tool_result: 1" in rendered
    assert "completion: 1" in rendered
    assert "message=bad" in rendered
