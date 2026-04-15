# Roadmap

## v0.1
- JSONL trace ingest
- normalized event model
- terminal timeline rendering
- basic secret redaction
- example trace and smoke tests

## v0.2
- run diff command
- event filtering by kind
- better summaries for commands and file writes
- markdown incident export

## v0.3
- source adapters for OpenClaw and generic coding-agent traces
- web timeline viewer
- replay metadata model

## v0.4
- causal analysis / root-cause hints
- policy checks for risky agent behavior
- searchable trace store

## v0.5
- live trace watching / streaming ingest
- incident-trigger rules for failing runs and regressions
- report bundles that can be emitted automatically when a run crosses an error threshold

## v0.6
- companion integrations built on top of Agent Black Box core
- Discord incident relay / private ops bot as a separate companion service, not bundled into core
- real-time posting of failure summaries, run links, and incident artifacts to an allowlisted ops room
- optional diff-versus-last-good-run alerting
