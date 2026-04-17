# Contributing

Thanks for checking out Agent Black Box.

## Current focus

Right now the project is in early MVP mode. The highest-value contributions are:
- trace adapters for real agent runtimes
- clearer event normalization
- better run diffing
- incident export improvements
- demo traces and reproducible examples
- UI work once the data model settles

## Development

```bash
uv sync --extra dev
uv run pytest -q
```

If you prefer plain venv + pip:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -e .[dev]
pytest -q
```

## Ground rules

- keep the core schema small and readable
- prefer explicit event normalization over magic heuristics
- do not add surveillance-y defaults or secret-leaking behavior
- local-first by default
- every new adapter should come with a fixture or example trace
- keep docs and demo artifacts aligned with the current CLI output
