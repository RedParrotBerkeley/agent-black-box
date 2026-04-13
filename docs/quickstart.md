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
PYTHONPATH=src python -m agent_black_box.cli summary examples/sample_trace.jsonl --redact
PYTHONPATH=src python -m agent_black_box.cli timeline examples/openclaw_trace.jsonl --format openclaw-jsonl
```

## 4. Run tests

```bash
PYTHONPATH=src pytest -q
```
