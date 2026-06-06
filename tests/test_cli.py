from pathlib import Path

from taskcli.cli import cmd_add, cmd_done


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
