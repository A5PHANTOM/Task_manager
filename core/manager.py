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
        tasks = self.storage.load_tasks()
        for task in tasks :
            if task.task_id == task_id :
                task.update_status(status)
                self.storage.save_all(tasks)
                return task
        raise TaskNotFount(f"Task {task_id} not Found")
    
    def delete_task(self,title : str):
        tasks = self.storage.load_tasks()
        new_tasks = [t for t in tasks if t.title != title]

        if len(tasks) == len(new_tasks):
            raise TaskNotFount(f"Task { title} not found")
        self.storage.save_all(new_tasks)

    def search_tasks(self, search_term: str):
        """Search tasks by title (case-insensitive partial match)"""
        tasks = self.storage.load_tasks()
        search_term_lower = search_term.lower()
        return [t for t in tasks if search_term_lower in t.title.lower()]
    
    def get_all_titles(self):
        """Get all task titles for autocomplete"""
        tasks = self.storage.load_tasks()
        return [t.title for t in tasks]




    
