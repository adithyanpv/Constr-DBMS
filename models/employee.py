# models/employee.py
from db import get_db_pool
from datetime import datetime,timezone

async def create_employee(employee):
    query = """
        INSERT INTO employees (e_name, designation, salary, manager_id)
        VALUES ($1, $2, $3, $4)
        RETURNING e_id, e_name, designation, salary, manager_id, created_at, updated_at
    """
    print("db_pool in create_employee:", get_db_pool)

    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, employee['e_name'], employee['designation'], employee['salary'], employee['manager_id'])
        return dict(row)

async def get_all_employees():
    query = "SELECT * FROM employees"
    async with get_db_pool().acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    
async def get_employee_by_id(employee_id: int):
    query = "SELECT * FROM employees WHERE e_id = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, employee_id)
        return dict(row) if row else None

async def update_employee(employee_id: int, employee_data: dict):
    now = datetime.now(timezone.utc)
    query = """
        UPDATE employees
        SET e_name = $1, designation = $2, salary = $3, manager_id = $4, updated_at = $5
        WHERE e_id = $6
        RETURNING e_id, e_name, designation, salary, manager_id, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query,
                                  employee_data['e_name'],
                                  employee_data['designation'],
                                  employee_data['salary'],
                                  employee_data['manager_id'],
                                  now,
                                  employee_id)
        return dict(row) if row else None

async def delete_employee(employee_id: int):
    query = """
        DELETE FROM employees
        WHERE e_id = $1
        RETURNING e_id, e_name, designation, salary, manager_id, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, employee_id)
        return dict(row) if row else None
