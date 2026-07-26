from fastapi import FastAPI, HTTPException, Path, Query
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
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

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


    

