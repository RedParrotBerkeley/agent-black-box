# Architecture

Agent Black Box is built around a simple pipeline:

1. **ingest** raw runtime events
2. **normalize** them into a stable trace schema
3. **render** timelines, diffs, and incident summaries
4. **redact** sensitive fields for safe sharing

## MVP components

- `parser.py` ingests JSONL traces into a normalized in-memory run model
- `models.py` defines trace events and runs
- `timeline.py` renders a readable event timeline
- `redaction.py` removes common secret-bearing fields
- `cli.py` exposes the first operator-facing interface

## Near-term additions

- file diff tracking
- command stdout/stderr capture summaries
- event classification by category
- run-to-run diffing
- adapter layer for source-specific traces
