# HN Package

## Recommended title

Show HN: Agent Black Box, a local-first flight recorder for AI agent runs

## Alternate titles

- Show HN: Agent Black Box, black-box forensics for coding agent runs
- Show HN: Agent Black Box, inspect and diff AI agent runs locally
- Show HN: Agent Black Box, incident reports for AI agent failures

## Submission body draft

I built Agent Black Box because I got tired of debugging agent failures through chat transcripts and scattered logs.

When a coding agent or tool-using assistant goes off the rails, the real question usually is not just "did it fail?" It is "what actually happened, in what order, and what changed between this run and the last one?"

Agent Black Box is an open source local-first CLI for runtime forensics on agent runs.

It ingests traces, normalizes them, and turns them into artifacts you can actually inspect:
- readable timelines
- focused run diffs
- incident-style summaries
- static reports you can share without pasting raw logs everywhere

Right now the strongest real-runtime support is for OpenClaw session JSONL, and I recently added support for real OpenClaw sessions instead of just toy example traces.

The current MVP supports:
- generic JSONL traces
- real OpenClaw session JSONL traces
- timeline rendering
- focused and raw diff views
- incident summary export
- static HTML reports
- basic redaction

It is still early. Replay, better diff alignment, and stronger root-cause hints are still ahead. But it is now useful enough that I wanted to put it in front of people building coding agents, MCP/tool-using assistants, or other long-running agent workflows.

Would especially love feedback on:
- what failure/debugging views are missing today
- what would make this more useful than just logs
- what other runtimes are worth supporting next

## First comment draft

A good way to understand the project quickly is:
- failure-case HTML report first
- real OpenClaw report second
- terminal GIF third

The current wedge is not "AI observability for everything." It is much narrower: local-first runtime forensics for powerful agent runs that are annoying to debug from transcripts alone.

## Likely reply drafts

### Why not just logs?

Because agent logs are usually incomplete, inconsistent, and hard to compare across runs. The useful thing is not raw event exhaust by itself. It is turning a run into a normalized timeline, a shareable incident artifact, and a comparison surface.

### Why local-first?

Because traces can contain prompts, tool arguments, paths, outputs, and sometimes secrets. I wanted the default mode to be inspect locally first, share selectively second.

### Why no full UI?

I deliberately started with CLI plus static artifacts because I wanted the trace model and artifacts to be solid before building a bigger interface around them. The HTML report is the first step toward a more product-like surface.

### How is this different from generic observability tools?

The main difference is the target object. I am not starting from generic logs, spans, or metrics. I am starting from the idea that an agent run is a thing you should be able to reconstruct, compare, and explain step by step.

### Is this production-ready?

Not as a broad platform. It is an early local-first MVP. But it is already useful for inspecting and sharing traces, especially for OpenClaw-style tool-using runs.
