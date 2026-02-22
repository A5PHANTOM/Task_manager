import argparse
from storage.json_storage import JSONStorage
from core.manager import TaskManager
from utils.file_ops import import_tasks_from_json,export_tasks_to_csv

storage = JSONStorage("data/tasks.json")
manager = TaskManager(storage)

parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command")

add = sub.add_parser("add")
add.add_argument("--title", required=True)
add.add_argument("--priority", default="medium")

args = parser.parse_args()

if args.command == "add":
    manager.add_task(args.title, args.priority)
    print("Task added")