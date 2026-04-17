from agent_black_box.html_report import render_html_report
from agent_black_box.parser import parse_jsonl_trace


def test_html_report_uses_failure_trace_metadata(tmp_path):
    trace = tmp_path / 'failure.jsonl'
    trace.write_text(
        '{"run_id":"r1","agent":"demo","ts":"1","kind":"tool_result","source":"exec","tool":"exec","message":"pytest failed","is_error":true}\n'
        '{"run_id":"r1","agent":"demo","ts":"2","kind":"completion","source":"assistant","message":"done"}\n'
    )
    run = parse_jsonl_trace(trace)

    html = render_html_report(
        title='Demo report',
        subtitle='Subtitle',
        timeline='timeline body',
        summary='summary body',
        diff='diff body',
        run=run,
        compare_run=None,
    )

    assert 'Failure' in html
    assert 'pytest failed' in html
    assert 'Top tool: exec' in html
    assert 'Run' in html and 'r1' in html
    assert 'pytest returned exit code 1' not in html


def test_html_report_handles_non_failure_run(tmp_path):
    trace = tmp_path / 'success.jsonl'
    trace.write_text(
        '{"run_id":"r2","agent":"demo","ts":"1","kind":"prompt","source":"user","message":"hello"}\n'
        '{"run_id":"r2","agent":"demo","ts":"2","kind":"completion","source":"assistant","message":"done"}\n'
    )
    run = parse_jsonl_trace(trace)

    html = render_html_report(
        title='Success report',
        subtitle='Subtitle',
        timeline='timeline body',
        summary='summary body',
        diff='diff body',
        run=run,
        compare_run=None,
    )

    assert 'Success' in html
    assert 'No explicit failure event; last event is completion' in html
    assert 'single run' in html


def test_html_report_shows_comparison_metadata(tmp_path):
    left = tmp_path / 'left.jsonl'
    right = tmp_path / 'right.jsonl'
    left.write_text('{"run_id":"left","agent":"demo","ts":"1","kind":"completion","source":"assistant","message":"done"}\n')
    right.write_text('{"run_id":"right","agent":"demo","ts":"1","kind":"warning","source":"assistant","message":"careful"}\n')
    run = parse_jsonl_trace(left)
    compare_run = parse_jsonl_trace(right)

    html = render_html_report(
        title='Compare report',
        subtitle='Subtitle',
        timeline='timeline body',
        summary='summary body',
        diff='diff body',
        run=run,
        compare_run=compare_run,
    )

    assert 'Compared with right' in html
    assert 'comparison enabled' in html
    assert 'Compare' in html and 'right' in html
