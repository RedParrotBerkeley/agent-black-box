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

Show HN: Agent Black Box, a local-first flight recorder for AI agent runs

I built Agent Black Box because I got tired of debugging agent failures through chat transcripts and scattered logs.

When a coding agent or tool-using assistant goes off the rails, the question usually is not just "did it fail?". The real question is "what actually happened, in what order, and what changed between this run and the last one?"

Agent Black Box is an open source local-first CLI that ingests runtime traces, normalizes them, and turns them into something inspectable:
- readable timelines
- focused run diffs
- incident-style summaries
- redacted artifacts you can share

Right now the MVP supports:
- generic JSONL traces
- real OpenClaw session JSONL traces
- legacy OpenClaw-style example traces
- timeline rendering
- incident summary export
- event-level diffing
- basic redaction

The newest step was adding support for real OpenClaw sessions instead of just toy example traces, plus compact and focused views so noisy real runs are easier to read.

I do not think the project is finished. Raw event diffing still needs better alignment for messy real-world runs, and replay/root-cause features are still ahead. But it is now at the point where it feels useful instead of hypothetical.

If you work on coding agents, MCP/tool-using assistants, or long-running agent workflows, I would love to know what trace/debugging features you wish existed.
