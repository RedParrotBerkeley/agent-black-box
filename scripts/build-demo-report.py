from __future__ import annotations

from pathlib import Path

from agent_black_box.html_report import render_html_report

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"

timeline = (DEMO / "openclaw-real-timeline.md").read_text()
summary = (DEMO / "openclaw-real-summary.md").read_text()
diff = (DEMO / "openclaw-real-diff.md").read_text()

html = render_html_report(
    title="Agent Black Box Report · OpenClaw Mission Control Run",
    subtitle="A static black-box report built from real OpenClaw demo artifacts, designed to be more legible and shareable than raw terminal output.",
    timeline=timeline,
    summary=summary,
    diff=diff,
)

out = DEMO / "openclaw-real-report.html"
out.write_text(html)
print(f"wrote {out}")
