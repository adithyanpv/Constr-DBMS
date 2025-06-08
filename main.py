'''from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import connect_to_db, disconnect_from_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db()
    yield
    await disconnect_from_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Construction Management App"}'''  
''' working 
from fastapi import FastAPI, HTTPException
from models.employee import (
    create_employee, get_all_employees, get_employee_by_id,
    update_employee, delete_employee
)
from schemas.employee import EmployeeCreate, EmployeeOut
from typing import List
from db import connect_to_db, disconnect_from_db
import asyncpg

# Lifespan context manager
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("▶️ Lifespan starting")
    await connect_to_db()
    print("✅ DB connected")
    yield
    await disconnect_from_db()
    print("🛑 DB disconnected")


app = FastAPI(lifespan=lifespan)

@app.post("/employees", response_model=EmployeeOut)
async def create_employee_endpoint(employee: EmployeeCreate):
    try:
        employee_data = employee.dict()
        new_employee = await create_employee(employee_data)
        return new_employee
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")

    except Exception as e:
        print(f"Error in create_employee_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@app.get("/employees", response_model=List[EmployeeOut])
async def get_all_employees_endpoint():
    try:
        employees = await get_all_employees()
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.get("/employees/{employee_id}", response_model=EmployeeOut)
async def get_employee_by_id_endpoint(employee_id: int):
    try:
        employee = await get_employee_by_id(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.put("/employees/{employee_id}", response_model=EmployeeOut)
async def update_employee_endpoint(employee_id: int, employee: EmployeeCreate):
    try:
        employee_data = employee.dict()
        updated_employee = await update_employee(employee_id, employee_data)
        if updated_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return updated_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@app.delete("/employees/{employee_id}", response_model=EmployeeOut)
async def delete_employee_endpoint(employee_id: int):
    try:
        deleted_employee = await delete_employee(employee_id)
        if deleted_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return deleted_employee
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
'''
'''
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from redis import add_employee, get_employee, delete_employee, add_employee_with_expiry
from db import get_db_pool
import asyncpg

# Define the Employee Pydantic model
class Employee(BaseModel):
    id: int
    name: str
    position: str
    department: str

app = FastAPI()

# Helper function to get the DB connection pool
def get_db():
    pool = get_db_pool()
    return pool

@app.post("/employees")
async def create_employee(employee: Employee, db = Depends(get_db)):
    # Create employee in the database
    async with db.acquire() as conn:
        query = """
        INSERT INTO Employees (id, name, position, department) 
        VALUES ($1, $2, $3, $4)
        """
        await conn.execute(query, employee.id, employee.name, employee.position, employee.department)

    # Cache the employee in Redis (without expiry)
    await add_employee(f"employee:{employee.id}", employee.dict())
    return {"message": "Employee created and cached successfully."}

@app.get("/employees/{employee_id}")
async def get_employee_data(employee_id: int, db = Depends(get_db)):
    # Try to get the employee from Redis first
    cached_employee = await get_employee(f"employee:{employee_id}")
    if cached_employee:
        return {"data": cached_employee, "source": "cache"}

    # If not found in Redis, fetch from the database
    async with db.acquire() as conn:
        query = "SELECT * FROM Employees WHERE id=$1"
        employee = await conn.fetchrow(query, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee_data = dict(employee)
        
        # Cache the employee data for future requests
        await add_employee(f"employee:{employee_id}", employee_data)
        return {"data": employee_data, "source": "database"}

@app.delete("/employees/{employee_id}")
async def delete_employee_data(employee_id: int, db = Depends(get_db)):
    # Delete the employee from the database
    async with db.acquire() as conn:
        query = "DELETE FROM Employees WHERE id=$1"
        result = await conn.execute(query, employee_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Employee not found")

    # Delete the employee from Redis cache
    await delete_employee(f"employee:{employee_id}")
    return {"message": "Employee deleted successfully."}

'''
# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import connect_to_db, disconnect_from_db
from routers.employees import router as employee_router
from routers.project import router as project_router
from routers.site import router as site_router
from routers.task import router as task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("▶️ Lifespan starting")
    await connect_to_db()
    print("✅ DB connected")
    yield
    await disconnect_from_db()
    print("🛑 DB disconnected")

app = FastAPI(lifespan=lifespan)

# Include router
app.include_router(employee_router)
app.include_router(project_router)
app.include_router(site_router)
app.include_router(task_router)
