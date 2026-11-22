"""Command-line interface for taskpad."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from . import __version__
from .storage import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskpad", description="A tiny command-line to-do manager."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--file", help="path to the task file (default: ~/.taskpad.json)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title", nargs="+", help="task description")

    p_list = sub.add_parser("list", help="show tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="include completed tasks")

    p_done = sub.add_parser("done", help="mark a task as completed")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="delete a task")
    p_rm.add_argument("id", type=int)

    sub.add_parser("clear", help="delete all completed tasks")
    return parser


def format_task(task) -> str:
    mark = "x" if task.done else " "
    return f"[{mark}] {task.id:>3}  {task.title}"


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        store = TaskStore(args.file)

        if args.command == "add":
            task = store.add(" ".join(args.title))
            print(f"Added #{task.id}: {task.title}")
        elif args.command == "list":
            tasks = [t for t in store.tasks if args.all or not t.done]
            if not tasks:
                print("Nothing to do. Nice!")
            for task in tasks:
                print(format_task(task))
        elif args.command == "done":
            task = store.complete(args.id)
            print(f"Completed #{task.id}: {task.title}")
        elif args.command == "rm":
            task = store.remove(args.id)
            print(f"Removed #{task.id}: {task.title}")
        elif args.command == "clear":
            print(f"Cleared {store.clear_done()} completed task(s).")
    except (KeyError, ValueError) as exc:
        print(f"error: {exc.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
