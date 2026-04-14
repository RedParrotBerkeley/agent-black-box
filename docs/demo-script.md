# Demo Script

This is the recommended terminal demo flow for Agent Black Box right now.

## Goal

Show three things, in this order:
1. a real run timeline
2. a clean incident summary
3. a focused comparison between two real runs

## Best command sequence

Play it live in the current terminal:

```bash
cd /Users/mpatraw1ax3ckps/.openclaw/workspace/agent-black-box
./scripts/demo-gif-sequence.sh play
```

Record a fresh cast/GIF/PNG automatically:

```bash
cd /Users/mpatraw1ax3ckps/.openclaw/workspace/agent-black-box
./scripts/demo-gif-sequence.sh record
```

## Exact execution order inside the script

```bash
agent-black-box timeline ~/.openclaw/agents/main/sessions/5522c802-eade-41d5-b67c-0179806b11bf.jsonl --format openclaw-jsonl --compact
agent-black-box summary ~/.openclaw/agents/main/sessions/5522c802-eade-41d5-b67c-0179806b11bf.jsonl --format openclaw-jsonl --compact
agent-black-box diff ~/.openclaw/agents/main/sessions/5522c802-eade-41d5-b67c-0179806b11bf.jsonl ~/.openclaw/agents/main/sessions/30572a54-78c4-4756-be4b-dfb18b1ccac5.jsonl --format openclaw-jsonl --compact --focus
```

## What to emphasize while recording

### Timeline

Say or imply:
- this is a real OpenClaw session, not a toy trace
- compact mode starts at the meaningful user prompt
- you can see tool calls and tool results in order
- the run ends in a concrete external action, a Discord message edit

### Summary

Say or imply:
- this gives you something shareable and incident-friendly
- setup noise is filtered out in compact mode
- key events and counts are visible at a glance

### Focused diff

Say or imply:
- this is the comparison view to demo first, not the raw event diff
- the point is to explain how two runs differ operationally
- for these runs, both reach the Discord edit step, but one explores more paths and uses extra tools

## Recording behavior

When you run `./scripts/demo-gif-sequence.sh record`, it will:
1. record the scripted terminal session to `demo/agent-black-box-demo.cast`
2. render a tuned GIF to `assets/demo.gif`
3. skip PNG generation cleanly on the current `agg 1.7.0` toolchain

## Terminal capture tips

- Use a large terminal window with generous padding before starting `record`
- Prefer a dark theme with high contrast
- Zoom in enough that headings are easy to read in GIF form
- The script now reduces idle time and speeds playback slightly for a tighter GIF
- If needed, you can tune rendering with env vars like `ABB_DEMO_FONT_SIZE`, `ABB_DEMO_ROWS`, `ABB_DEMO_COLS`, and `ABB_DEMO_SPEED`

## Recommended framing sentence

"Agent Black Box is a local-first flight recorder for AI agent runs. It turns real runtime traces into readable timelines, incident summaries, and focused run comparisons."

## Current strongest artifact order

1. `demo/openclaw-real-timeline.md`
2. `demo/openclaw-real-summary.md`
3. `demo/openclaw-real-diff.md`
