# Quickstart

## 1. Create a virtual environment

```bash
python3.13 -m venv .venv
. .venv/bin/activate
```

## 2. Install test dependency

```bash
python -m pip install pytest
```

## 3. Run the example commands

```bash
PYTHONPATH=src python -m agent_black_box.cli timeline examples/sample_trace.jsonl --redact
PYTHONPATH=src python -m agent_black_box.cli diff examples/sample_trace.jsonl examples/sample_trace_fixed.jsonl
PYTHONPATH=src python -m agent_black_box.cli diff examples/sample_trace.jsonl examples/sample_trace_fixed.jsonl --focus
PYTHONPATH=src python -m agent_black_box.cli summary examples/sample_trace.jsonl --redact
PYTHONPATH=src python -m agent_black_box.cli timeline examples/openclaw_trace.jsonl --format openclaw-jsonl
```

## 4. Run against a real OpenClaw session

```bash
PYTHONPATH=src python -m agent_black_box.cli timeline ~/.openclaw/agents/main/sessions/<session>.jsonl --format openclaw-jsonl --compact
PYTHONPATH=src python -m agent_black_box.cli summary ~/.openclaw/agents/main/sessions/<session>.jsonl --format openclaw-jsonl --compact --output incident.md
PYTHONPATH=src python -m agent_black_box.cli diff ~/.openclaw/agents/main/sessions/<run-a>.jsonl ~/.openclaw/agents/main/sessions/<run-b>.jsonl --format openclaw-jsonl --compact --focus
```

Notes:
- real OpenClaw session files live under `~/.openclaw/agents/main/sessions/`
- the `openclaw-jsonl` adapter supports both the old example format and real session JSONL
- real sessions are noisier than examples, so `timeline --compact` and `summary --compact` are usually the best first demo
- use `diff --compact --focus` when you want a comparison story instead of a raw event-by-event dump
- `--compact` is the recommended presentation mode for real sessions

## 5. Run tests

```bash
PYTHONPATH=src pytest -q
```
