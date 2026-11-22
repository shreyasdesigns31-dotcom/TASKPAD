"""JSON-backed storage for tasks."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path


def default_path() -> Path:
    """Where tasks live: $TASKPAD_FILE if set, else ~/.taskpad.json."""
    env = os.environ.get("TASKPAD_FILE")
    return Path(env) if env else Path.home() / ".taskpad.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created: str = field(
        default_factory=lambda: datetime.now().isoformat(timespec="seconds")
    )


class TaskStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else default_path()
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return [Task(**item) for item in data]
        except (json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"Could not read task file {self.path}: {exc}") from exc

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(t) for t in self.tasks]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty")
        next_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(id=next_id, title=title)
        self.tasks.append(task)
        self.save()
        return task

    def get(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}")

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self.save()
        return task

    def remove(self, task_id: int) -> Task:
        task = self.get(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def clear_done(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        self.save()
        return before - len(self.tasks)
