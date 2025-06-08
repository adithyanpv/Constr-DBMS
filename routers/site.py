from fastapi import APIRouter, HTTPException
from schemas.site import SiteCreate, SiteOut
import asyncpg
from models.site import (
    create_site, get_all_sites, get_site_by_id, update_site, delete_site
)
from typing import List
from schemas.site import SiteCreate,SiteOut
router = APIRouter(
    prefix="/sites",
    tags=["Site"]
)

@router.post("/", response_model=SiteOut)
async def create_site_endpoint(site: SiteCreate):
    try:
        site_data = site.model_dump()
        new_site = await create_site(site_data)
        return new_site
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    except Exception as e:
        print(f"Error in create_project_endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/", response_model=List[SiteOut])
async def get_all_site_endpoint():
    try:
        site = await get_all_sites()
        return site
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{site_id}", response_model=SiteOut)
async def get_site_by_id_endpoint(site_id: int):
    try:
        site = await get_site_by_id(site_id)
        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        return site
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.put("/{site_id}", response_model=SiteOut)
async def update_site_endpoint(site_id: int, site: SiteCreate):
    try:
        site_data = site.model_dump()
        updated_site = await update_site(site_id, site_data)
        if updated_site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        return updated_site
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/{site_id}", response_model=SiteOut)
async def delete_site_endpoint(site_id: int):
    try:
        deleted_site = await delete_site(site_id)
        if deleted_site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        return deleted_site
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

