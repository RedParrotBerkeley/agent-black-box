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


def test_parse_real_openclaw_session_jsonl(tmp_path):
    trace = tmp_path / "openclaw-session.jsonl"
    trace.write_text(
        '\n'.join(
            [
                '{"type":"session","version":3,"id":"sess-123","timestamp":"2026-04-14T12:00:00Z","cwd":"/tmp/project"}',
                '{"type":"model_change","id":"m1","parentId":null,"timestamp":"2026-04-14T12:00:00Z","provider":"openai-codex","modelId":"gpt-5.4"}',
                '{"type":"message","id":"u1","parentId":"m1","timestamp":"2026-04-14T12:00:01Z","message":{"role":"user","content":[{"type":"text","text":"Fix the failing PR"}]}}',
                '{"type":"message","id":"a1","parentId":"u1","timestamp":"2026-04-14T12:00:02Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"tc1","name":"exec","arguments":{"command":"pytest -q"}}],"stopReason":"toolUse"}}',
                '{"type":"message","id":"t1","parentId":"a1","timestamp":"2026-04-14T12:00:03Z","message":{"role":"toolResult","toolCallId":"tc1","toolName":"exec","content":[{"type":"text","text":"tests failed"}],"details":{"exitCode":1},"isError":true}}',
                '{"type":"message","id":"a2","parentId":"t1","timestamp":"2026-04-14T12:00:04Z","message":{"role":"assistant","content":[{"type":"text","text":"Pytest failed on one assertion"}],"stopReason":"endTurn"}}',
            ]
        )
        + '\n'
    )

    run = parse_trace(trace, source_format="openclaw-jsonl")

    assert run.run_id == "sess-123"
    assert run.session_id == "sess-123"
    assert run.agent == "openclaw"
    assert [event.kind for event in run.events] == [
        "session_start",
        "model_change",
        "prompt",
        "tool_call",
        "tool_result",
        "assistant_message",
    ]
    assert run.events[2].data["message"] == "Fix the failing PR"
    assert run.events[3].data["tool"] == "exec"
    assert run.events[3].data["arguments"] == {"command": "pytest -q"}
    assert run.events[4].data["tool_call_id"] == "tc1"
    assert run.events[4].data["is_error"] is True
    assert run.events[5].data["message"] == "Pytest failed on one assertion"
