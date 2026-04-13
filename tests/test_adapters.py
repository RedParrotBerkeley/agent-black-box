from agent_black_box.adapters import parse_trace


def test_parse_openclaw_jsonl_smoke(tmp_path):
    trace = tmp_path / "openclaw.jsonl"
    trace.write_text(
        '{"session_id":"s1","agent":"openclaw","ts":"1","event":"tool_call","source":"github","tool":"gh pr checks"}\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")

    assert run.run_id == "s1"
    assert run.agent == "openclaw"
    assert run.events[0].kind == "tool_call"
    assert run.events[0].data["tool"] == "gh pr checks"
