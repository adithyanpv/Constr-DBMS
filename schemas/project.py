#schemas/project.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    project_name:str
    no_of_workers: int
    proj_manager_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    project_id: int
    created_at : datetime
    updated_at: datetime