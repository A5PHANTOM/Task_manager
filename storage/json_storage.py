import json
from pathlib import Path
from core.models import Task
class JSONStorage:
    def __init__(self,file_path: str):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text('[]')

    def load_tasks(self):
        with open(self.file_path,'r') as file :
            data = json.load(file)


        tasks = []
        for item in data :
            task = Task(
                task_id=item["task_id"],
                title =item["title"],
                status = item["status"],
                priority=item["priority"]
            )
            tasks.append(task)

        return tasks
    

    def save_task(self,task):
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_all(tasks)

    def save_all(self,tasks):
        with open(self.file_path,'w') as file :
            json.dump (
                [task.to_dict() for task in tasks],
                file,
                indent=4
            )

    def get_next_id(self):
        tasks = self.load_tasks()
        if not tasks:
            return 1 
        return max(task.task_id for task in tasks ) +1 


