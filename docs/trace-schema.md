# Trace Schema

The MVP normalized event model uses these top-level fields:

- `run_id`: stable run identifier
- `agent`: agent or runtime name
- `session_id`: optional session/thread identifier
- `ts`: event timestamp
- `kind`: normalized event kind
- `source`: source runtime or subsystem
- additional event-specific fields stored in `data`

## Example kinds

- `prompt`
- `tool_call`
- `tool_result`
- `command`
- `file_write`
- `diff`
- `warning`
- `failure`
- `completion`

The goal is to let multiple runtimes map into one readable timeline without forcing the UI to understand every raw source format directly.
