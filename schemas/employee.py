# schemas/employee.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    e_name: str
    designation: Optional[str]
    salary: Optional[float]
    manager_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    e_id: int
    created_at: datetime
    updated_at: datetime
