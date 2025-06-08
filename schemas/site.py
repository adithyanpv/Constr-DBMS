from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SiteBase(BaseModel):
    location:str
    site_manager_id: Optional[int] = None

class SiteCreate(SiteBase):
    pass

class SiteOut(SiteBase):
    site_id: int
    created_at: datetime
    updated_at: datetime
