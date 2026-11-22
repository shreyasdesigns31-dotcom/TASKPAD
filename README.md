# taskpad

A tiny command-line to-do manager. No dependencies, one JSON file, zero fuss.

```
$ taskpad add buy milk
Added #1: buy milk
$ taskpad add finish report
Added #2: finish report
$ taskpad done 1
Completed #1: buy milk
$ taskpad list
[ ]   2  finish report
```

## Install

```bash
git clone https://github.com/shreyasdesigns31-dotcom/taskpad.git
cd taskpad
pip install -e .
```

## Usage

| Command | What it does |
|---|---|
| `taskpad add <title...>` | Add a task |
| `taskpad list [-a]` | Show open tasks (`-a` includes completed) |
| `taskpad done <id>` | Mark a task completed |
| `taskpad rm <id>` | Delete a task |
| `taskpad clear` | Delete all completed tasks |

Tasks are stored in `~/.taskpad.json`. Override with the `TASKPAD_FILE`
environment variable or the `--file` flag.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Ideas for contributions

- Due dates and priorities
- Tags and filtering
- Colored output
- `taskpad edit <id>`

## License

MIT
