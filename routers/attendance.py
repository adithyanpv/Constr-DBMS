from fastapi import APIRouter, HTTPException
from schemas.attendance import AttendanceCreate, AttendanceOut
from models.attendance import (
    create_attendance,
    get_all_attendance,
    get_attendance_by_id,
    update_attendance,
    delete_attendance,
)
from typing import List
import asyncpg

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.post("/", response_model=AttendanceOut)
async def create_attendance_endpoint(attendance: AttendanceCreate):
    try:
        attendance_data = attendance.model_dump()
        new_attendance = await create_attendance(attendance_data)
        return new_attendance
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Attendance already marked for this employee and date.")
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="Invalid employee ID or site ID.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/", response_model=List[AttendanceOut])
async def get_all_attendance_endpoint():
    try:
        attendance =  await get_all_attendance()
        return attendance
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{attendance_id}", response_model=AttendanceOut)
async def get_attendance_by_id_endpoint(attendance_id: int):
    try:
        attendance = await get_attendance_by_id(attendance_id)
        if attendance is None:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return attendance
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.put("/{attendance_id}", response_model=AttendanceOut)
async def update_attendance_endpoint(attendance_id: int, attendance: AttendanceCreate):
    try:
        updated = await update_attendance(attendance_id, attendance.model_dump())
        if updated is None:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return updated
    except asyncpg.exceptions.ForeignKeyViolationError:
        raise HTTPException(status_code=400, detail="Invalid employee ID or site ID.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/{attendance_id}", response_model=AttendanceOut)
async def delete_attendance_endpoint(attendance_id: int):
    try:
        deleted = await delete_attendance(attendance_id)
        if deleted is None:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return deleted
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
