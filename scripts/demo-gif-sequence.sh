#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LEFT="$HOME/.openclaw/agents/main/sessions/5522c802-eade-41d5-b67c-0179806b11bf.jsonl"
RIGHT="$HOME/.openclaw/agents/main/sessions/30572a54-78c4-4756-be4b-dfb18b1ccac5.jsonl"

export PYTHONPATH=src
PY=python3.13

clear
printf '\n\n'
echo '$ agent-black-box timeline ~/.openclaw/.../5522c802...jsonl --format openclaw-jsonl --compact'
sleep 1
$PY -m agent_black_box.cli timeline "$LEFT" --format openclaw-jsonl --compact

sleep 2
printf '\n\n'
echo '$ agent-black-box summary ~/.openclaw/.../5522c802...jsonl --format openclaw-jsonl --compact'
sleep 1
$PY -m agent_black_box.cli summary "$LEFT" --format openclaw-jsonl --compact

sleep 2
printf '\n\n'
echo '$ agent-black-box diff ~/.openclaw/.../5522c802...jsonl ~/.openclaw/.../30572a54...jsonl --format openclaw-jsonl --compact --focus'
sleep 1
$PY -m agent_black_box.cli diff "$LEFT" "$RIGHT" --format openclaw-jsonl --compact --focus
