import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from taskcli.tasks import Task


def save_tasks(tasks: list[Task], path: Path) -> None:
    # Write the list of tasks to a JSON file at path
    serialized = [_task_to_dict(t) for t in tasks]
    path.write_text(json.dumps(serialized, indent=2))


def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    return [_dict_to_task(d) for d in raw]


def _task_to_dict(task: Task) -> dict:
    data = asdict(task)
    data["created_at"] = task.created_at.isoformat()
    return data


def _dict_to_task(data: dict) -> Task:
    return Task(
        title=data["title"],
        done=data["done"],
        id=data["id"],
        created_at=datetime.fromisoformat(data["created_at"]),
    )
