from datetime import datetime

class Task:
    def __init__(self,task_id : int ,title :str,status="pending",priority="medium"):
        self.task_id = task_id
        self.title = title
        self.status = status
        self.priority = priority
        self.created_at = datetime.now()


    def update_status(self,new_status : str):
        if new_status not in ("pending","in_progress","completed"):
            raise ValueError("Invalid task status")
        self.status = new_status

    def to_dict(self):
        return{
            "task_id": self.task_id,
            "title" : self.title,
            "status" : self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat()
        }