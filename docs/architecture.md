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

## Companion-service direction

A likely v2 direction is to keep Agent Black Box core focused on ingest, normalization, diffing, and incident artifact generation, while building live operational surfaces as separate companion services.

The clearest candidate is a Discord incident relay:
- watch traces or runtime events in near real time
- detect failures, regressions, or policy-triggering runs
- post short incident summaries into a private allowlisted Discord ops room
- optionally attach or link a rendered report bundle
- optionally compare a failing run against the last known good run

Important design choice: this should live outside the core repository as a companion integration unless the core API boundary becomes stable enough to justify first-party packaging. The core product should remain the black-box engine; live chat surfaces should sit on top of it.
