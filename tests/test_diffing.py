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

    assert "difference 1:" in rendered
    assert "echo bad" in rendered
    assert "echo good" in rendered
