from agent_black_box.filtering import filter_run
from agent_black_box.parser import parse_jsonl_trace


def test_filter_run_keeps_only_requested_kinds(tmp_path):
    trace = tmp_path / "trace.jsonl"
    trace.write_text(
        '{"run_id":"r1","ts":"1","kind":"prompt","source":"assistant","message":"hi"}\n'
        '{"run_id":"r1","ts":"2","kind":"command","source":"shell","command":"echo hi"}\n'
    )

    run = parse_jsonl_trace(trace)
    filtered = filter_run(run, ["command"])

    assert len(filtered.events) == 1
    assert filtered.events[0].kind == "command"
