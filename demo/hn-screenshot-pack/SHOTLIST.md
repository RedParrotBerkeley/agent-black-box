# HN Screenshot Shotlist

Primary recommended image order:
1. `failure-report.html`
2. `demo.gif`
3. optional: `failure-timeline.md`

## Shot 1: failure-report hero
- Open `failure-report.html` in a browser.
- Capture the hero section plus the top of the timeline card.
- Keep the visible frame focused on:
  - title
  - failure badges
  - highlighted "pytest returned exit code 1"
  - first timeline events

## Shot 2: full failure report context
- Slightly wider crop showing:
  - hero
  - timeline
  - incident summary
- This is the best "what the project is" screenshot.

## Shot 3: terminal credibility shot
- Open `failure-timeline.md` in terminal/editor.
- Keep visible lines:
  - prompt
  - `tool=exec`
  - `is_error=True`
  - `exitCode=1`
  - assistant explanation

## Optional real-run follow-up
- If you have a fresh real OpenClaw session trace, also build a real-run report and capture it as the realism proof.
