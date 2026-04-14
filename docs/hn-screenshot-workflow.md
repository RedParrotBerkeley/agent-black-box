# HN Screenshot Workflow

Use the bundled script to generate the HN screenshot pack:

```bash
cd /path/to/agent-black-box
./scripts/hn-screenshot-pack.sh
```

Artifacts will be written to:
- `demo/hn-screenshot-pack/`

Open these first:
- `demo/hn-screenshot-pack/failure-report.html`
- `demo/hn-screenshot-pack/demo.gif`
- `demo/hn-screenshot-pack/SHOTLIST.md`

## If you want a real-run screenshot too

Pass a real OpenClaw session path as `REAL_TRACE`:

```bash
cd /path/to/agent-black-box
REAL_TRACE="$HOME/.openclaw/agents/main/sessions/<session>.jsonl" ./scripts/hn-screenshot-pack.sh
```

That will additionally generate:
- `demo/hn-screenshot-pack/real-timeline.md`
- `demo/hn-screenshot-pack/real-summary.md`
- `demo/hn-screenshot-pack/real-report.html`

## Best screenshot order for HN

1. failure report hero (`failure-report.html`)
2. failure report wider context
3. optional terminal credibility shot (`failure-timeline.md`)
4. GIF as supporting asset

## Why this order

The failure report is the most immediately legible artifact. It shows the problem, the failing step, and the value of the tool in one frame.
