from __future__ import annotations

from collections import Counter
from html import escape

from agent_black_box.models import TraceRun


def render_html_report(
    *,
    title: str,
    subtitle: str,
    timeline: str,
    summary: str,
    diff: str,
    run: TraceRun,
    compare_run: TraceRun | None = None,
) -> str:
    badges = _build_badges(run, compare_run)
    meta_boxes = _build_meta_boxes(run, compare_run)
    highlights = _build_highlights(run, compare_run)

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{escape(title)}</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #11182d;
      --panel-2: #0f1527;
      --text: #e8edf7;
      --muted: #9fb0d1;
      --line: #24304d;
      --accent: #7dd3fc;
      --accent-2: #a78bfa;
      --good: #86efac;
      --warn: #fbbf24;
      --danger: #f87171;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif;
      background: radial-gradient(circle at top, #121a31 0%, var(--bg) 45%);
      color: var(--text);
    }}
    .wrap {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 28px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: linear-gradient(180deg, rgba(125,211,252,0.08), rgba(167,139,250,0.04));
      box-shadow: 0 20px 60px rgba(0,0,0,0.35);
      margin-bottom: 22px;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -80px -80px auto;
      width: 240px;
      height: 240px;
      background: radial-gradient(circle, rgba(125,211,252,0.18), rgba(125,211,252,0));
      pointer-events: none;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 40px;
      line-height: 1.02;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 17px;
      max-width: 900px;
      line-height: 1.6;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }}
    .card {{
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    }}
    .span-12 {{ grid-column: span 12; }}
    .span-6 {{ grid-column: span 6; }}
    .section-label {{
      display: inline-block;
      margin-bottom: 12px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(125,211,252,0.12);
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    pre {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace;
      font-size: 13px;
      line-height: 1.55;
      color: #e6edf9;
    }}
    .callout {{
      margin-top: 16px;
      padding: 14px 16px;
      border: 1px solid rgba(134,239,172,0.2);
      border-radius: 14px;
      background: rgba(134,239,172,0.06);
      color: #d9ffe5;
      font-size: 14px;
      line-height: 1.55;
    }}
    .hero-badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      border: 1px solid rgba(125,211,252,0.18);
      background: rgba(12,18,34,0.55);
      color: var(--text);
    }}
    .badge-danger {{
      border-color: rgba(248,113,113,0.28);
      background: rgba(248,113,113,0.10);
      color: #ffd8d8;
    }}
    .badge-good {{
      border-color: rgba(134,239,172,0.28);
      background: rgba(134,239,172,0.10);
      color: #dbffe8;
    }}
    .badge-warn {{
      border-color: rgba(251,191,36,0.28);
      background: rgba(251,191,36,0.10);
      color: #ffeebf;
    }}
    .meta-strip {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 18px 0 0;
    }}
    .meta-box {{
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid rgba(125,211,252,0.14);
      background: rgba(12,18,34,0.45);
    }}
    .meta-k {{
      font-size: 11px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 6px;
    }}
    .meta-v {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }}
    .highlight-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }}
    .highlight-box {{
      padding: 14px 16px;
      border-radius: 16px;
      border: 1px solid rgba(248,113,113,0.16);
      background: linear-gradient(180deg, rgba(248,113,113,0.10), rgba(17,24,45,0.85));
    }}
    .highlight-label {{
      font-size: 11px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #ffb3b3;
      margin-bottom: 6px;
    }}
    .highlight-value {{
      font-size: 15px;
      font-weight: 700;
      color: #fff1f1;
    }}
    .footer {{
      color: var(--muted);
      margin-top: 18px;
      font-size: 13px;
    }}
    @media (max-width: 980px) {{
      .span-6 {{ grid-column: span 12; }}
      .meta-strip {{ grid-template-columns: 1fr; }}
      .highlight-grid {{ grid-template-columns: 1fr; }}
      h1 {{ font-size: 30px; }}
    }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <section class=\"hero\">
      <div class=\"eyebrow\">Agent Black Box</div>
      <h1>{escape(title)}</h1>
      <div class=\"subtitle\">{escape(subtitle)}</div>
      <div class=\"callout\">{escape(_callout_text(run, compare_run))}</div>
      <div class=\"hero-badges\">
        {badges}
      </div>
      <div class=\"meta-strip\">
        {meta_boxes}
      </div>
      <div class=\"highlight-grid\">
        {highlights}
      </div>
    </section>

    <section class=\"grid\">
      <article class=\"card span-6\">
        <div class=\"section-label\">Timeline</div>
        <pre>{escape(timeline)}</pre>
      </article>

      <article class=\"card span-6\">
        <div class=\"section-label\">Summary</div>
        <pre>{escape(summary)}</pre>
      </article>

      <article class=\"card span-12\">
        <div class=\"section-label\">Focused Diff</div>
        <pre>{escape(diff)}</pre>
        <div class=\"footer\">Generated locally from trace data. Use redaction before sharing when the run may contain secrets or internal paths.</div>
      </article>
    </section>
  </div>
</body>
</html>
"""


def _callout_text(run: TraceRun, compare_run: TraceRun | None) -> str:
    status = _run_status(run)
    base = (
        f"This static report reflects the actual trace for run {run.run_id} "
        f"with {run.event_count} event(s) from {run.agent or 'an unknown agent'}."
    )
    if compare_run is not None:
        return base + f" Comparison mode is enabled against {compare_run.run_id}. Primary status: {status}."
    return base + f" Primary status: {status}."


def _build_badges(run: TraceRun, compare_run: TraceRun | None) -> str:
    items: list[tuple[str, str]] = []
    status = _run_status(run)
    status_class = {
        'failure': 'badge-danger',
        'warning': 'badge-warn',
        'success': 'badge-good',
    }.get(status, '')
    items.append((status.title(), status_class))
    items.append((f"{run.event_count} event{'s' if run.event_count != 1 else ''}", ''))
    if compare_run is not None:
        items.append((f"Compared with {compare_run.run_id}", ''))
    top_tool = _top_tool(run)
    if top_tool:
        items.append((f"Top tool: {top_tool}", ''))
    return "\n        ".join(
        f'<div class="badge {css}">{escape(text)}</div>'.replace('  ', ' ').replace('badge "', 'badge"')
        if css
        else f'<div class="badge">{escape(text)}</div>'
        for text, css in items
    )


def _build_meta_boxes(run: TraceRun, compare_run: TraceRun | None) -> str:
    boxes = [
        ("Run", run.run_id),
        ("Agent", run.agent or "unknown"),
        ("Compare", compare_run.run_id if compare_run is not None else "none"),
    ]
    return "\n        ".join(
        f'<div class="meta-box"><div class="meta-k">{escape(label)}</div><div class="meta-v">{escape(value)}</div></div>'
        for label, value in boxes
    )


def _build_highlights(run: TraceRun, compare_run: TraceRun | None) -> str:
    highlights = [
        ("Primary incident", _primary_incident(run)),
        ("Top event kind", _top_event_kind(run)),
        ("Diff mode", "comparison enabled" if compare_run is not None else "single run"),
    ]
    return "\n        ".join(
        f'<div class="highlight-box"><div class="highlight-label">{escape(label)}</div><div class="highlight-value">{escape(value)}</div></div>'
        for label, value in highlights
    )


def _run_status(run: TraceRun) -> str:
    if any(event.kind == 'failure' or event.data.get('is_error') is True for event in run.events):
        return 'failure'
    if any(event.kind == 'warning' for event in run.events):
        return 'warning'
    if any(event.kind == 'completion' for event in run.events):
        return 'success'
    return 'unknown'


def _primary_incident(run: TraceRun) -> str:
    for event in run.events:
        if event.kind == 'failure' or event.data.get('is_error') is True:
            detail = event.data.get('message') or event.data.get('content') or event.data.get('command') or event.kind
            return _clip(str(detail), 80)
    if run.events:
        return f"No explicit failure event; last event is {run.events[-1].kind}"
    return 'No events captured'


def _top_tool(run: TraceRun) -> str | None:
    counts = Counter(event.data.get('tool') for event in run.events if event.data.get('tool'))
    if not counts:
        return None
    return counts.most_common(1)[0][0]


def _top_event_kind(run: TraceRun) -> str:
    if not run.events:
        return 'none'
    counts = Counter(event.kind for event in run.events)
    kind, count = counts.most_common(1)[0]
    return f"{kind} ({count})"


def _clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + '...'
