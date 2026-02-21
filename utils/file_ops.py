import json
import csv
from core.models import Task

def import_tasks_from_json(file_path, manager):
    with open(file_path, "r") as file:
        data = json.load(file)

    for item in data:
        manager.add_task(
            title=item["title"],
            priority=item.get("priority", "medium")
        )

def task_generator(tasks):
    for task in tasks:
        yield [
            task.task_id,
            task.title,
            task.status,
            task.priority,
            task.created_at
        ]
        
def export_tasks_to_csv(file_path, tasks):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["ID", "Title", "Status", "Priority", "Created At"]
        )

        for row in task_generator(tasks):
            writer.writerow(row)

