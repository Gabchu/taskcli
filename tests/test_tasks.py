from datetime import datetime
from pathlib import Path

from taskcli.tasks import Task, add_task
from taskcli.storage import load_tasks, save_tasks

def test_add_task_has_given_title():
    task = add_task("Buy milk")
    assert task.title == "Buy milk"

def test_new_task_is_not_done():
    task = add_task("Buy milk")
    assert task.done is False

def test_each_task_gets_a_unique_id():
    a = add_task("Task A")
    b = add_task("Task B")
    assert a.id != b.id
    assert a.id #not empty

def test_task_records_creation_time():
    task = add_task("Buy milk")
    assert isinstance(task.created_at, datetime) #isinstance(x, datetime) checks "is x a datetime object?"

def test_load_returns_empty_list_when_file_missing(tmp_path: Path):
    db = tmp_path / "tasks.json"
    assert load_tasks(db) == []

def test_save_then_load_round_trips(tmp_path: Path):
    db = tmp_path / "tasks.json"
    original = [add_task("Buy milk"), add_task("Walk dog")]
    save_tasks(original, db)
    assert load_tasks(db) == original