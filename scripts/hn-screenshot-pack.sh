#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3.13}"
PYTHONPATH_VALUE="${PYTHONPATH_VALUE:-src}"
SCREENSHOT_DIR="${SCREENSHOT_DIR:-demo/hn-screenshot-pack}"
FAILURE_TRACE="${FAILURE_TRACE:-demo/openclaw-failure-trace.jsonl}"
REAL_TRACE="${REAL_TRACE:-}"

mkdir -p "$SCREENSHOT_DIR"

echo "[1/6] Building failure-case CLI artifacts"
PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli timeline "$FAILURE_TRACE" \
  --format openclaw-jsonl --compact --output "$SCREENSHOT_DIR/failure-timeline.md"
PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli summary "$FAILURE_TRACE" \
  --format openclaw-jsonl --compact --output "$SCREENSHOT_DIR/failure-summary.md"
PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli report "$FAILURE_TRACE" \
  --format openclaw-jsonl --compact \
  --output "$SCREENSHOT_DIR/failure-report.html" \
  --title "Agent Black Box Report · Failing Test Run" \
  --subtitle "A failure-focused black-box report showing an agent encountering a failing pytest run and surfacing the error path cleanly."

echo "[2/6] Copying current GIF demo"
cp assets/demo.gif "$SCREENSHOT_DIR/demo.gif"

echo "[3/6] Copying HN launch copy"
cp docs/hn-package.md "$SCREENSHOT_DIR/hn-package.md"

echo "[4/6] Writing screenshot checklist"
cat > "$SCREENSHOT_DIR/SHOTLIST.md" <<'EOF'
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
EOF

echo "[5/6] Building real-run artifact if REAL_TRACE is set"
if [[ -n "$REAL_TRACE" ]]; then
  PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli timeline "$REAL_TRACE" \
    --format openclaw-jsonl --compact --output "$SCREENSHOT_DIR/real-timeline.md"
  PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli summary "$REAL_TRACE" \
    --format openclaw-jsonl --compact --output "$SCREENSHOT_DIR/real-summary.md"
  PYTHONPATH="$PYTHONPATH_VALUE" "$PYTHON_BIN" -m agent_black_box.cli report "$REAL_TRACE" \
    --format openclaw-jsonl --compact \
    --output "$SCREENSHOT_DIR/real-report.html" \
    --title "Agent Black Box Report · Real OpenClaw Run" \
    --subtitle "A real OpenClaw run rendered as a black-box artifact for debugging, sharing, and incident review."
else
  echo "REAL_TRACE not set; skipping real-run report build"
fi

echo "[6/6] Done"
echo
echo "Artifacts written to: $SCREENSHOT_DIR"
echo "Open these first:"
echo "- $SCREENSHOT_DIR/failure-report.html"
echo "- $SCREENSHOT_DIR/demo.gif"
echo "- $SCREENSHOT_DIR/SHOTLIST.md"
