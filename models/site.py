from db import get_db_pool
from datetime import datetime, timezone

async def create_site(site):
    query = """
        INSERT INTO site (location,site_manager_id)
        VALUES ($1, $2)
        RETURNING site_id,location, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query,site['location'],site['site_manager_id'])
        return dict(row)

async def get_all_sites():
    query = "SELECT * FROM site"
    async with get_db_pool().acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

async def get_site_by_id(site_id: int):
    query = "SELECT * FROM site WHERE site_id = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, site_id)
        return dict(row) if row else None

async def update_site(site_id: int, site_data: dict):
    now = datetime.now(timezone.utc)
    query = """
        UPDATE site
        SET  location = $1, updated_at = $2
        WHERE site_id = $3
        RETURNING site_id, location, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, site_data['location'], now, site_id)
        return dict(row) if row else None

async def delete_site(site_id: int):
    query = """
        DELETE FROM site
        WHERE site_id = $1
        RETURNING site_id,location, created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, site_id)
        return dict(row) if row else None
