from storage.json_storage import JSONStorage
from core.manager import TaskManager

storage = JSONStorage("data/tasks.json")
manager = TaskManager(storage)

task1 = manager.add_task("Learn FastAPI","high")
task2 = manager.add_task("Build projects","medium")

tasks = manager.list_tasks()

for t in tasks:
    print(t.task_id ,t.title,t.status)