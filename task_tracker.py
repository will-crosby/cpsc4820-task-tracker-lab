"""Task Tracker — a small command-line task manager.

CPSC 4820/6820 Week 4 starter project.

This is a deliberately simple, working program. Your job in Assignment 4.1
is NOT to fix this code by hand — it is to delegate a feature or improvement
to an AI agent (on a branch!) and supervise the work. See the assignment
document for ideas and requirements.

Usage:
    python task_tracker.py add "Buy groceries"
    python task_tracker.py add "Study for exam" --tag school
    python task_tracker.py list
    python task_tracker.py list --tag school
    python task_tracker.py done 2
    python task_tracker.py delete 3
    python task_tracker.py stats
"""

import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.environ.get("TASK_TRACKER_FILE", "tasks.json")


def load_tasks():
    """Load the task list from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Write the task list to the JSON data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    """Return the next available task id."""
    return max((t["id"] for t in tasks), default=0) + 1


def add_task(tasks, title, tag=None):
    """Add a new task and return it."""
    task = {
        "id": next_id(tasks),
        "title": title,
        "tag": tag,
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
        "completed": None,
    }
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    """Mark the task with the given id as done. Returns the task or None."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            task["completed"] = datetime.now().isoformat(timespec="seconds")
            return task
    return None


def delete_task(tasks, task_id):
    """Delete the task with the given id. Returns True if deleted."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False


def filter_tasks(tasks, tag=None, include_done=True):
    """Return tasks, optionally filtered by tag and completion state."""
    result = tasks
    if tag is not None:
        result = [t for t in result if t.get("tag") == tag]
    if not include_done:
        result = [t for t in result if not t["done"]]
    return result


def stats(tasks):
    """Return a small summary dict of the task list."""
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    tags = {}
    for t in tasks:
        if t.get("tag"):
            tags[t["tag"]] = tags.get(t["tag"], 0) + 1
    return {"total": total, "done": done, "open": total - done, "by_tag": tags}


def format_task(task):
    """Format a single task for terminal display."""
    mark = "x" if task["done"] else " "
    tag = f"  #{task['tag']}" if task.get("tag") else ""
    return f"[{mark}] {task['id']:>3}  {task['title']}{tag}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="A tiny task tracker.")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Add a task")
    p_add.add_argument("title")
    p_add.add_argument("--tag", default=None)

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--tag", default=None)
    p_list.add_argument("--open", action="store_true", help="Hide completed tasks")

    p_done = sub.add_parser("done", help="Mark a task complete")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)

    sub.add_parser("stats", help="Show summary statistics")

    args = parser.parse_args(argv)
    tasks = load_tasks()

    if args.command == "add":
        task = add_task(tasks, args.title, args.tag)
        save_tasks(tasks)
        print(f"Added task {task['id']}: {task['title']}")
    elif args.command == "list":
        for task in filter_tasks(tasks, args.tag, include_done=not args.open):
            print(format_task(task))
    elif args.command == "done":
        task = complete_task(tasks, args.id)
        save_tasks(tasks)
        if task:
            print(f"Completed: {task['title']}")
        else:
            print(f"No task with id {args.id}")
    elif args.command == "delete":
        if delete_task(tasks, args.id):
            save_tasks(tasks)
            print(f"Deleted task {args.id}")
        else:
            print(f"No task with id {args.id}")
    elif args.command == "stats":
        s = stats(tasks)
        print(f"Total: {s['total']}  Open: {s['open']}  Done: {s['done']}")
        for tag, count in sorted(s["by_tag"].items()):
            print(f"  #{tag}: {count}")
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
