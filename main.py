from fastapi import FastAPI, HTTPException, Path, Query, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Task(BaseModel):

    id: int
    title: str
    done: bool = False

SEED_TASKS: list[Task] = [

    Task(id=1, title="Make cheese!", done=False),
    Task(id=2, title="Make pizza", done=True),
    Task(id=3, title="Make burger", done=True)

]

@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks", "/stats"]}

@app.get("/health")
async def health_check():
    return {"status": "ok" }

@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return SEED_TASKS

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_with_id(task_id: int = Path(..., description="ID of the task in the queue.", examples=[1])):

    for task in SEED_TASKS:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail=f"Task {task_id} not found!")

@app.get("/stats", response_model=list[Task])
async def get_stats():

    completed=[]
    for task in SEED_TASKS:
        if task.done == True:
            completed.append(task)
    
    return completed

@app.post("/tasks")
async def create_task(title: str = Body(..., embed=True, description="Task title.", examples=["Make pasta"])):

    task_id = len(SEED_TASKS) + 1
    task = Task(id=task_id, title=title, done=False)
    SEED_TASKS.append(task)

    return JSONResponse(status_code=201, content={"message": "Created!"})
    
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int = Path(..., description="The ID of the task to update."), 
                      new_title: str = Body(..., embed=True, description="New title of the task.")):

    for task in SEED_TASKS:
        if task.id == task_id:
            task.title = new_title
            return task

    raise HTTPException(status_code=404, detail="Unknown ID")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int = Path(..., description="ID of the task.")):

    for index, task in enumerate(SEED_TASKS):
        if task.id == task_id:
            SEED_TASKS.pop(index)
            return JSONResponse(status_code=204, content={"message": "No Content"})

    raise HTTPException(status_code=404, detail="Unknown ID.")





    

