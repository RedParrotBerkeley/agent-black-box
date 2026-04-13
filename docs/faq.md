# FAQ

## Is this a memory system?

No. Agent Black Box is for runtime telemetry, replay, diffing, and incident reporting.

## Is this the same as Fredsidian?

No. Fredsidian is about long-term assistant memory and context architecture. Agent Black Box is about what happened during a run.

## Why local-first?

Because traces can contain sensitive prompts, commands, paths, outputs, and secrets.

## Why not just use logs?

Because most agent logs are incomplete, inconsistent, and hard to compare across runs. This project aims to normalize the run into something you can actually inspect.
