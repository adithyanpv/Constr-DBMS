# models/project.py
from db import get_db_pool
from datetime import datetime,timezone
async def create_project(project):
    query = """
           INSERT INTO project(project_name,no_of_workers,proj_manager_id)
           VALUES ($1, $2, $3)
           RETURNING project_id,project_name,no_of_workers,proj_manager_id,created_at,updated_at
           """
    print("db_pool in create_employee:", get_db_pool)
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(
        query,
        project["project_name"],
        project["no_of_workers"],
        project["proj_manager_id"]
    )
    return dict(row)

async def get_all_projects():
    query = "SELECT * FROM project"
    async with get_db_pool().acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

async def get_project_by_id(project_id:int):
    query = "SELECT * FROM employees WHERE project_id = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, project_id)
        return dict(row) if row else None

async def update_project(project_id: int, project_data: dict):
    now = datetime.now(timezone.utc)
    query = """
        UPDATE employees
        SET project_name = $1, no_of_workers = $2, proj_manager_id = $3,  updated_at = $4
        WHERE project_id = $5
        RETURNING project_id, project_name, no_of_workers, proj_manager_id, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query,
                                  project_data['project_name'],
                                  project_data['no-of_workers'],
                                  project_data['proj_manager_id'],
                                  now,
                                  project_id)
        return dict(row) if row else None

async def delete_project(project_id: int):
    query = """
        DELETE FROM project
        WHERE project_id = $1
        RETURNING project_id, project_name, no_of_workers, proj_manager_id, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, project_id)
        return dict(row) if row else None