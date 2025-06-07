# routers/employees.py

from fastapi import APIRouter, HTTPException
from typing import List
import asyncpg

from models.employee import (
    create_employee, get_all_employees, get_employee_by_id,
    update_employee, delete_employee
)
from schemas.employee import EmployeeCreate, EmployeeOut

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeOut)
async def create_employee_endpoint(employee: EmployeeCreate):
    try:
        employee_data = employee.model_dump()
        new_employee = await create_employee(employee_data)
        return new_employee
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    except Exception as e:
        print(f"Error in create_employee_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/", response_model=List[EmployeeOut])
async def get_all_employees_endpoint():
    try:
        employees = await get_all_employees()
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee_by_id_endpoint(employee_id: int):
    try:
        employee = await get_employee_by_id(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.put("/{employee_id}", response_model=EmployeeOut)
async def update_employee_endpoint(employee_id: int, employee: EmployeeCreate):
    try:
        employee_data = employee.model_dump()
        updated_employee = await update_employee(employee_id, employee_data)
        if updated_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return updated_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/{employee_id}", response_model=EmployeeOut)
async def delete_employee_endpoint(employee_id: int):
    try:
        deleted_employee = await delete_employee(employee_id)
        if deleted_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return deleted_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
