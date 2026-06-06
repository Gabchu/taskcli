from dataclasses import dataclass, field, replace
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    title: str
    done: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


def add_task(title: str) -> Task:
    return Task(title=title)


def mark_done(task: Task) -> Task:
    return replace(task, done=True)
