from fastapi import FastAPI,HTTPException,Depends
from storage.json_storage import JSONStorage
from core.manager import TaskManager
from core.exceptions import TaskNotFount
from storage.db_storage import DBStorage #for db storage

app = FastAPI()

# storage = JSONStorage("data/tasks.json") #for json 
storage = DBStorage()
manager = TaskManager(storage)


@app.get("/tasks")
def get_tasks():
    return [t.to_dict() for t in manager.list_tasks()]

@app.post("/tasks")
def create_task(task : dict):
    return manager.add_task(task["title"],task.get("priority","medium")).to_dict()

@app.put("/tasks/{task_id}")
def update_task(task_id : int , body : dict ):
    try:
        return manager.update_task_status(task_id,body["status"]).to_dict()
    except TaskNotFount:
        raise HTTPException(status_code=404, detail="Task not found")
    
@app.delete("/tasks/{task_id}")
def delete_task(task_id : int ):
    try:
        manager.delete_task(task_id)
        return{"message":"task deleted !!"}
    except TaskNotFount:
        raise HTTPException(status_code=404, detail="Task not found")
    
