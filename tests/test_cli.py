from pathlib import Path

from taskcli.cli import cmd_add, cmd_delete, cmd_done


def test_cmd_add_persists_a_task(tmp_path: Path):
    db = tmp_path / "tasks.json"

    cmd_add("Buy milk", db)

    from taskcli.cli import load_tasks

    tasks = load_tasks(db)
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"


def test_cmd_done_marks_the_matching_task(tmp_path: Path):
    db = tmp_path / "tasks.json"
    cmd_add("Buy milk", db)

    from taskcli.storage import load_tasks

    task_id = load_tasks(db)[0].id

    cmd_done(task_id[:4], db)

    assert load_tasks(db)[0].done is True


def test_cmd_done_reports_when_no_match(tmp_path: Path, capsys):
    db = tmp_path / "tasks.json"
    cmd_add("Buy milk", db)

    cmd_done("zzzz", db)
    captured = capsys.readouterr()

    assert "No task found" in captured.out

def test_cmd_delete_removes_the_matching_task(tmp_path: Path):
    db = tmp_path / "tasks.json"
    cmd_add("Task A", db)
    cmd_add("Task B", db)

    from taskcli.storage import load_tasks
    task_a_id = load_tasks(db)[0].id
    cmd_delete(task_a_id[:4], db)

    remaining = load_tasks(db)
    assert len(remaining) == 1
    assert remaining[0].title == "Task B"

def test_cmd_delete_reports_when_no_match(tmp_path: Path, capsys):
    db = tmp_path / "tasks.json"
    cmd_add("Buy milk", db)

    cmd_delete("zzzz", db)

    captured = capsys.readouterr()
    assert "No task found" in captured.out