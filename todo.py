import argparse
import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return []


def save_tasks(tasks):
    DATA_FILE.write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Keep track of small tasks.")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("text")
    commands.add_parser("list")
    for name in ("done", "remove"):
        command = commands.add_parser(name)
        command.add_argument("id", type=int)
    args = parser.parse_args()

    try:
        tasks = load_tasks()
        if args.command == "add":
            text = args.text.strip()
            if not text:
                parser.error("Task cannot be empty.")
            task_id = max((task["id"] for task in tasks), default=0) + 1
            tasks.append({"id": task_id, "text": text, "done": False})
            save_tasks(tasks)
            print(f"Added task {task_id}.")
        elif args.command == "list":
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                status = "x" if task["done"] else " "
                print(f"{task['id']}. [{status}] {task['text']}")
        else:
            task = next((task for task in tasks if task["id"] == args.id), None)
            if task is None:
                parser.error("Task ID not found.")
            if args.command == "done":
                task["done"] = True
                print(f"Completed task {args.id}.")
            else:
                tasks.remove(task)
                print(f"Removed task {args.id}.")
            save_tasks(tasks)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Could not read or save tasks: {error}\n")


if __name__ == "__main__":
    main()
