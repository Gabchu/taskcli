# taskcli

A tiny command-line task manager, built as a Python learning project.

Stores tasks in a local JSON file. Supports add, list, mark-done, and delete.

## Quickstart

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Gabchu/taskcli.git
cd taskcli
uv sync
```

## Usage

```bash
uv run taskcli add "Buy milk"
uv run taskcli add "Walk dog"
uv run taskcli list
uv run taskcli done <id-prefix>
uv run taskcli delete <id-prefix>
```

`<id-prefix>` is any unique starting substring of the task id, just like a Git short hash.

By default, tasks are stored at `~/.taskcli/.tasks.json`. Override with `--db /custom/path.json`.

## Development

Run the tests:

```bash
uv run pytest
```

Run the linter and formatter:

```bash
uv run ruff check .
uv run ruff format .
```

## Project layout

- `src/taskcli/tasks.py` — `Task` dataclass and pure domain functions.
- `src/taskcli/storage.py` — JSON persistence.
- `src/taskcli/cli.py` — argparse-based CLI.
- `tests/` — pytest suite.

## License

MIT
