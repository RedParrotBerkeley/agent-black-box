# Quickstart

## 1. Install dependencies

Using `uv`:

```bash
uv sync --extra dev
```

Or with a plain virtual environment:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
```

## 2. Run the example commands

```bash
uv run python -m agent_black_box.cli timeline examples/sample_trace.jsonl --redact
uv run python -m agent_black_box.cli diff examples/sample_trace.jsonl examples/sample_trace_fixed.jsonl
uv run python -m agent_black_box.cli diff examples/sample_trace.jsonl examples/sample_trace_fixed.jsonl --focus
uv run python -m agent_black_box.cli summary examples/sample_trace.jsonl --redact
uv run python -m agent_black_box.cli report demo/openclaw-failure-trace.jsonl --format openclaw-jsonl --compact --redact --output report.html
uv run python -m agent_black_box.cli timeline examples/openclaw_trace.jsonl --format openclaw-jsonl
```

## 3. Run against a real OpenClaw session

```bash
uv run python -m agent_black_box.cli timeline ~/.openclaw/agents/main/sessions/<session>.jsonl --format openclaw-jsonl --compact
uv run python -m agent_black_box.cli summary ~/.openclaw/agents/main/sessions/<session>.jsonl --format openclaw-jsonl --compact --output incident.md
uv run python -m agent_black_box.cli diff ~/.openclaw/agents/main/sessions/<run-a>.jsonl ~/.openclaw/agents/main/sessions/<run-b>.jsonl --format openclaw-jsonl --compact --focus
```

Notes:
- real OpenClaw session files live under `~/.openclaw/agents/main/sessions/`
- the `openclaw-jsonl` adapter supports both the old example format and real session JSONL
- real sessions are noisier than examples, so `timeline --compact` and `summary --compact` are usually the best first demo
- use `diff --compact --focus` when you want a comparison story instead of a raw event-by-event dump
- `--compact` is the recommended presentation mode for real sessions

## 4. Run tests

```bash
uv run pytest -q
```

## 5. Build distributable artifacts

```bash
uv build
```
