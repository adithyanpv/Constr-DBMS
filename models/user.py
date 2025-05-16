from db import get_db_pool
from datetime import datetime, timezone

async def create_user(user: dict):
    query = """
        INSERT INTO users (username, hashed_password, role, created_at)
        VALUES ($1, $2, $3, $4)
        RETURNING userid, username, role, created_at
    """
    async with get_db_pool().acquire() as conn:
        now = datetime.now(timezone.utc)
        row = await conn.fetchrow(query, user['username'], user['hashed_password'], user['role'], now)
        return dict(row)

async def get_user_by_username(username: str):
    query = "SELECT * FROM users WHERE username = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, username)
        return dict(row) if row else None

async def get_user_by_id(userid: int):
    query = "SELECT userid, username, role, created_at FROM users WHERE userid = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, userid)
        return dict(row) if row else None
