# Demo Script

## 60-second demo

1. Show failing run timeline
2. Show fixed run diff
3. Show incident summary export
4. Explain why this is better than plain logs

## Terminal flow

```bash
agent-black-box timeline examples/sample_trace.jsonl --redact
agent-black-box diff examples/sample_trace.jsonl examples/sample_trace_fixed.jsonl
agent-black-box summary examples/sample_trace.jsonl --redact
agent-black-box timeline examples/openclaw_trace.jsonl --format openclaw-jsonl
```

## Talking points

- agents need flight recorders, not just chat history
- debugging needs structure, not transcript archaeology
- redaction matters if traces are going to be shared
- run diffing is how you find the first bad step quickly
