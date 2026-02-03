from core.models import Task
from core.exceptions import TaskNotFount

class TaskManager:
    def __init__(self,storage):
        self.storage = storage

    def add_task(self,
                 title : str,
                 priority : str ="medium"):
        task_id = self.storage.get_next_id()
        task = Task(task_id,title,priority=priority)
        self.storage.save_task(task)
        return task
    
    def list_tasks(self, status = None):
        tasks = self.storage.load_tasks()
        if status :
            return [t for t in tasks if t.status == status ]
        return tasks
    

    def update_task_status(self,task_id : int, status : str ):
        tasks = self.storage.load()
        for task in tasks :
            if task.task_id == task_id :
                task.update_status(status)
                self.storage.save_all(tasks)
                return task
        raise TaskNotFount(f"Task {task_id} not Found")
    
    def delete_task(self,task_id : int):
        tasks = self.storage.load_task()
        new_tasks = [t for t in tasks if t.task_id != task_id]

        if len(tasks) == len(new_tasks):
            raise TaskNotFount(f"Task { task_id} not found")
        self.storage.save_all(new_tasks)




    
