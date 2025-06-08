from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from datetime import datetime

class AttendanceBase(BaseModel):
    e_id: int
    date: date
    check_in_time: Optional[time] = None
    check_out_time: Optional[time] = None
    present: bool
    site_id: int

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    attendance_id: int
    created_at: Optional[datetime] = None  # Optional if you're adding timestamps
    updated_at: Optional[datetime] = None
