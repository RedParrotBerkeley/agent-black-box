#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LEFT="${ABB_DEMO_LEFT:-$HOME/.openclaw/agents/main/sessions/5522c802-eade-41d5-b67c-0179806b11bf.jsonl}"
RIGHT="${ABB_DEMO_RIGHT:-$HOME/.openclaw/agents/main/sessions/30572a54-78c4-4756-be4b-dfb18b1ccac5.jsonl}"
PY="${ABB_DEMO_PYTHON:-python3.13}"
CAST_PATH="${ABB_DEMO_CAST_PATH:-$ROOT/demo/agent-black-box-demo.cast}"
GIF_PATH="${ABB_DEMO_GIF_PATH:-$ROOT/assets/demo.gif}"
PNG_PATH="${ABB_DEMO_PNG_PATH:-$ROOT/assets/demo.png}"
AGG_THEME="${ABB_DEMO_THEME:-nord}"
AGG_FONT_SIZE="${ABB_DEMO_FONT_SIZE:-18}"
AGG_ROWS="${ABB_DEMO_ROWS:-26}"
AGG_COLS="${ABB_DEMO_COLS:-110}"
AGG_SPEED="${ABB_DEMO_SPEED:-1.15}"
AGG_IDLE_LIMIT="${ABB_DEMO_IDLE_LIMIT:-1.2}"
AGG_LAST_FRAME_DURATION="${ABB_DEMO_LAST_FRAME_DURATION:-1.6}"
MODE="${1:-play}"

export PYTHONPATH=src

run_demo() {
  printf '$ agent-black-box demo\n'
  sleep 0.15
  "$PY" -m agent_black_box.cli timeline "$LEFT" --format openclaw-jsonl --compact --banner | sed -n '1,18p'
  sleep 0.45
  printf '\n'
  echo '$ agent-black-box timeline ~/.openclaw/.../5522c802...jsonl --format openclaw-jsonl --compact'
  sleep 0.25
  "$PY" -m agent_black_box.cli timeline "$LEFT" --format openclaw-jsonl --compact

  sleep 0.65
  printf '\n\n'
  echo '$ agent-black-box summary ~/.openclaw/.../5522c802...jsonl --format openclaw-jsonl --compact'
  sleep 0.25
  "$PY" -m agent_black_box.cli summary "$LEFT" --format openclaw-jsonl --compact

  sleep 0.65
  printf '\n\n'
  echo '$ agent-black-box diff ~/.openclaw/.../5522c802...jsonl ~/.openclaw/.../30572a54...jsonl --format openclaw-jsonl --compact --focus'
  sleep 0.25
  "$PY" -m agent_black_box.cli diff "$LEFT" "$RIGHT" --format openclaw-jsonl --compact --focus
}

record_demo() {
  command -v asciinema >/dev/null 2>&1 || { echo 'missing dependency: asciinema' >&2; exit 1; }
  command -v agg >/dev/null 2>&1 || { echo 'missing dependency: agg' >&2; exit 1; }

  mkdir -p "$(dirname "$CAST_PATH")" "$(dirname "$GIF_PATH")"

  asciinema rec --overwrite --command "$0 play" "$CAST_PATH"
  agg \
    --theme "$AGG_THEME" \
    --font-size "$AGG_FONT_SIZE" \
    --rows "$AGG_ROWS" \
    --cols "$AGG_COLS" \
    --speed "$AGG_SPEED" \
    --idle-time-limit "$AGG_IDLE_LIMIT" \
    --last-frame-duration "$AGG_LAST_FRAME_DURATION" \
    "$CAST_PATH" "$GIF_PATH"

  echo
  echo "wrote $CAST_PATH"
  echo "wrote $GIF_PATH"
  echo "note: PNG preview generation skipped because agg 1.7.0 does not support --last-frame output"
}

show_help() {
  cat <<'EOF'
Usage:
  ./scripts/demo-gif-sequence.sh            # play the demo sequence in the current terminal
  ./scripts/demo-gif-sequence.sh play       # same as above
  ./scripts/demo-gif-sequence.sh record     # record the sequence with asciinema and render assets/demo.gif via agg

Optional environment overrides:
  ABB_DEMO_LEFT        path to left/session trace
  ABB_DEMO_RIGHT       path to comparison trace
  ABB_DEMO_PYTHON      python executable (default: python3.13)
  ABB_DEMO_CAST_PATH   output .cast path
  ABB_DEMO_GIF_PATH    output GIF path
  ABB_DEMO_PNG_PATH    output PNG preview path
EOF
}

case "$MODE" in
  play)
    run_demo
    ;;
  record)
    record_demo
    ;;
  -h|--help|help)
    show_help
    ;;
  *)
    echo "unknown mode: $MODE" >&2
    show_help >&2
    exit 2
    ;;
esac
