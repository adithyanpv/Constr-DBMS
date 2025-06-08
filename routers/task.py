from fastapi import APIRouter, HTTPException
from typing import List
import asyncpg

from models.task import(create_task,get_all_tasks,get_task_by_id,update_task,delete_task)
from schemas.task import TaskCreate,TaskOut

router = APIRouter(prefix= "/task",tags =["Task"])

@router.post("/", response_model=TaskOut)
async def create_task_endpoint(task: TaskCreate):
    try:
        task_data = task.model_dump()
        new_task = await create_task(task_data)
        return new_task
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="Invalid project_id. Project does not exist.")
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    except Exception as e:
        print(f"Error in create_task_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/", response_model=List[TaskOut])
async def get_all_tasks_endpoint():
    try:
        tasks = await get_all_tasks()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{task_id}", response_model=TaskOut)
async def get_task_by_id_endpoint(task_id: int):
    try:
        task = await get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.put("/{task_id}", response_model=TaskOut)
async def update_task_endpoint(task_id: int, task: TaskCreate):
    try:
        task_data = task.model_dump()
        updated_task = await update_task(task_id, task_data)
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/{task_id}", response_model=TaskOut)
async def delete_task_endpoint(task_id: int):
    try:
        deleted_task = await delete_task(task_id)
        if deleted_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return deleted_task
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")