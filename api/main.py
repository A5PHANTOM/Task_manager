from fastapi import FastAPI,HTTPException,Depends,UploadFile,File
from fastapi.responses import FileResponse
from storage.json_storage import JSONStorage
from core.manager import TaskManager
from core.exceptions import TaskNotFount
from storage.db_storage import DBStorage #for db storage
from utils.file_ops import import_tasks_from_json, export_tasks_to_csv
import json
import os

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
    
@app.delete("/tasks/{title}")
def delete_task(title : str ):
    try:
        manager.delete_task(title)
        return{"message":"task deleted !!"}
    except TaskNotFount:
        raise HTTPException(status_code=404, detail="Task not found")
    
@app.post("/import")
async def import_tasks(file: UploadFile = File(...)):
    """Import tasks from a JSON file"""
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed")
    
    try:
        # Save uploaded file temporarily
        temp_path = f"data/temp_import_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Import tasks
        import_tasks_from_json(temp_path, manager)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {"message": "Tasks imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@app.get("/export")
def export_tasks():
    """Export all tasks to a CSV file"""
    try:
        output_path = "data/export_tasks.csv"
        tasks = manager.list_tasks()
        
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks to export")
        
        export_tasks_to_csv(output_path, tasks)
        
        return FileResponse(
            path=output_path,
            media_type="text/csv",
            filename="tasks_export.csv"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@app.get("/search")
def search_tasks(q: str):
    """Search tasks by title (partial match)"""
    if not q:
        raise HTTPException(status_code=400, detail="Search query is required")
    
    results = manager.search_tasks(q)
    return [t.to_dict() for t in results]

@app.get("/titles")
def get_all_titles():
    """Get all task titles for autocomplete"""
    return {"titles": manager.get_all_titles()}

