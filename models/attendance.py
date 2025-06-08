from db import get_db_pool
from datetime import datetime,timezone

# Create new attendance record
async def create_attendance(attendance: dict):
    query = """
        INSERT INTO attendance (e_id,  date, check_in_time, check_out_time, present,site_id)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING attendance_id, e_id, date, check_in_time, check_out_time, present, site_id,created_at, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(
            query,
            attendance["e_id"],
            attendance["date"],
            attendance.get("check_in_time"),
            attendance.get("check_out_time"),
            attendance["present"],
            attendance["site_id"]  
        )
        return dict(row)

# Get all attendance records
async def get_all_attendance():
    query = "SELECT * FROM attendance ORDER BY date DESC"
    async with get_db_pool().acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

# Get a single attendance record by ID
async def get_attendance_by_id(attendance_id: int):
    query = "SELECT * FROM attendance WHERE attendance_id = $1"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, attendance_id)
        return dict(row) if row else None

# Update attendance record
async def update_attendance(attendance_id: int, data: dict):
    now = datetime.now(timezone.utc)
    query = """
        UPDATE attendance
        SET e_id = $1, date = $2,
            check_in_time = $3, check_out_time = $4, present = $5,site_id =$6,updated_at = $7
        WHERE attendance_id = $8
        RETURNING attendance_id, e_id, date, check_in_time, check_out_time, present,site_id, updated_at
    """
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(
            query,
            data["e_id"],
            data["date"],
            data.get("check_in_time"),
            data.get("check_out_time"),
            data["present"],
            data["site_id"],
            now,
            attendance_id
        )
        return dict(row) if row else None

# Delete attendance record
async def delete_attendance(attendance_id: int):
    query = "DELETE FROM attendance WHERE attendance_id = $1 RETURNING *"
    async with get_db_pool().acquire() as conn:
        row = await conn.fetchrow(query, attendance_id)
        return dict(row) if row else None
