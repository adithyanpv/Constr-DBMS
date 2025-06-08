# schemas/employee.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,date

class TaskBase(BaseModel):
    task_name: str
    description: Optional[str]
    project_id: int
    assigned_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    task_id: int
    created_at: datetime
    updated_at: datetime
