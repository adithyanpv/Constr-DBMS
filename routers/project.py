from fastapi import APIRouter, HTTPException
from typing import List
import asyncpg

from models.project import(
    create_project,get_all_projects,get_project_by_id,update_project,delete_project
)
from schemas.project import ProjectCreate,ProjectOut
router = APIRouter(prefix = "/project",tags =["Project"])

@router.post("", response_model= ProjectOut)
async def create_employee_endpoint(project: ProjectCreate):
    try:
        project_data = project.model_dump()
        new_project = await create_project(project_data)
        return new_project
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    except Exception as e:
        print(f"Error in create_project_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("", response_model=List[ProjectOut])
async def get_all_project_endpoint():
    try:
        project = await get_all_projects()
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id_endpoint(project_id: int):
    try:
        project = await get_project_by_id(project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.put("/{project_id}", response_model=ProjectOut)
async def update_project_endpoint(project_id: int, project: ProjectCreate):
    try:
        project_data = project.model_dump()
        updated_project = await update_project(project_id, project_data)
        if updated_project is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return updated_project
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/{project_id}", response_model=ProjectOut)
async def delete_project_endpoint(project_id: int):
    try:
        deleted_project = await delete_project(project_id)
        if deleted_project is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return deleted_project
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

