# models/task.py
from db import get_db_pool
from datetime import datetime, timezone

async def create_task(task):
    query = """
        INSERT INTO task (task_name, description, project_id, assigned_date, due_date, status)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING task_id, task_name, description, project_id, assigned_date, due_date, status, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(
            query,
            task["task_name"],
            task.get("description"),
            task["project_id"],
            task.get("assigned_date"),
            task.get("due_date"),
            task.get("status"),
        )
        return dict(row)

async def get_all_tasks():
    query = "SELECT * FROM task"
    async with get_db_pool().acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

async def get_task_by_id(task_id: int):
    query = "SELECT * FROM task WHERE task_id = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, task_id)
        return dict(row) if row else None

async def update_task(task_id: int, task_data: dict):
    query = """
        UPDATE task
        SET task_name = $1,
            description = $2,
            project_id = $3,
            assigned_date = $4,
            due_date = $5,
            status = $6,
            updated_at = $7
        WHERE task_id = $8
        RETURNING task_id, task_name, description, project_id, assigned_date, due_date, status, created_at, updated_at
    """
    now = datetime.now(timezone.utc)
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(
            query,
            task_data["task_name"],
            task_data.get("description"),
            task_data["project_id"],
            task_data.get("assigned_date"),
            task_data.get("due_date"),
            task_data.get("status"),
            now,
            task_id
        )
        return dict(row) if row else None

async def delete_task(task_id: int):
    query = """
        DELETE FROM task
        WHERE task_id = $1
        RETURNING task_id, task_name, description, project_id, assigned_date, due_date, status, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, task_id)
        return dict(row) if row else None
