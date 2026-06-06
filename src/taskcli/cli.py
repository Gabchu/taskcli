import argparse
from pathlib import Path

from taskcli.storage import load_tasks, save_tasks
from taskcli.tasks import add_task, delete_task, mark_done

DEFAULT_DB = Path.home() / ".taskcli" / ".tasks.json"


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    args.db.parent.mkdir(parents=True, exist_ok=True)

    if args.command == "add":
        cmd_add(args.title, args.db)
    elif args.command == "list":
        cmd_list(args.db)
    elif args.command == "done":
        cmd_done(args.id_prefix, args.db)
    elif args.command == "delete":
        cmd_delete(args.id_prefix, args.db)
    else:
        parser.print_help()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskcli",
        description="A task manager",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"Path to the JSON store (default: {DEFAULT_DB})",
    )

    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task title")

    subparsers.add_parser("list", help="List all tasks")

    done_p = subparsers.add_parser("done", help="Mark a task as done")
    done_p.add_argument("id_prefix", help="Task id (or any unique prefix)")

    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id_prefix", help="Task id (or any unique prefix)")

    return parser


def cmd_add(title: str, db: Path) -> None:
    tasks = load_tasks(db)
    task = add_task(title)
    tasks.append(task)
    save_tasks(tasks, db)
    print(f"Added: {task.title} (id: {task.id[:8]})")


def cmd_list(db: Path) -> None:
    tasks = load_tasks(db)
    if not tasks:
        print("No tasks yet")
        return
    for t in tasks:
        box = "[x]" if t.done else "[ ]"
        print(f"{box} {t.id[:8]} {t.title}")


def cmd_done(id_prefix: str, db: Path) -> None:
    tasks = load_tasks(db)
    matches = [t for t in tasks if t.id.startswith(id_prefix)]
    if not matches:
        print(f"No task found with id starting with {id_prefix!r}")
        return
    if len(matches) > 1:
        print(f"Ambiguous: {len(matches)} tasks match {id_prefix!r}. Be more specific.")
        return

    target = matches[0]
    updated = [mark_done(t) if t is target else t for t in tasks]
    save_tasks(updated, db)
    print(f"Marked done: {target.title}")

def cmd_delete(id_prefix: str, db: Path) -> None:
    tasks = load_tasks(db)
    matches = [t for t in tasks if t.id.startswith(id_prefix)]
    if not matches:
        print(f"No task found with id starting with {id_prefix!r}")
        return
    if len(matches) > 1:
        print(f"Ambiguous: {len(matches)} tasks match {id_prefix!r}. Be more specific.")
        return
    
    target = matches[0]
    updated = delete_task(tasks, target.id)
    save_tasks(updated, db)
    print(f"Deleted {target.title}")