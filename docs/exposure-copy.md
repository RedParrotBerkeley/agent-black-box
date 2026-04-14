# Exposure Copy

## Short tagline

Flight recorder, replay, diff, and incident reporting for AI agent runs.

## One-liner

Agent Black Box helps you understand what an AI agent actually did, where it failed, and what changed between runs.

## Launch post draft

Built a new open source project: **Agent Black Box**.

It is a flight recorder for AI agent runs.

Instead of treating agent failures like mysterious chat glitches, it captures normalized runtime events so you can:
- inspect a timeline
- diff two runs
- export incident summaries
- audit tool calls, commands, and failures

Current MVP supports:
- JSONL traces
- real OpenClaw session traces and legacy OpenClaw-style traces
- timeline rendering
- run diffing
- incident summary export
- basic redaction

The goal is simple: make agent debugging feel more like systems debugging and less like guessing.

## Show HN draft

Show HN: Agent Black Box, a flight recorder for AI agent runs

I built Agent Black Box to answer a problem I kept running into with coding agents and tool-using assistants: when a run goes wrong, plain logs and chat transcripts usually do a poor job explaining what actually happened.

The project is a local-first trace ingestor and CLI that can currently:
- ingest JSONL traces
- normalize events
- render a timeline
- diff two runs
- export an incident summary
- ingest real OpenClaw session traces

The longer-term goal is replay, smarter diffing for noisy real runs, root-cause hints, and adapters for more agent runtimes.
