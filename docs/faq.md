# FAQ

## Is this a memory system?

No. Agent Black Box is for runtime telemetry, replay, diffing, and incident reporting.

## Is this the same as Fredsidian?

No. Fredsidian is about long-term assistant memory and context architecture. Agent Black Box is about what happened during a run.

## Why local-first?

Because traces can contain sensitive prompts, commands, paths, outputs, and secrets.

## Why not just use logs?

Because most agent logs are incomplete, inconsistent, and hard to compare across runs. This project aims to normalize the run into something you can actually inspect.

## Is this ready for production incident response?

Not fully. It is an early local-first MVP that is already useful for inspection and sharing, but replay, stronger diff alignment, and deeper root-cause help are still ahead.

## What real runtimes does it support today?

Right now the strongest real-runtime story is OpenClaw session JSONL support. Generic JSONL traces are also supported.
