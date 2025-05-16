from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username:str
class UserCreate(UserBase):
    password:str
    role: str

class UserOut(UserBase):
  user_id:int
  role: str
  created_at : datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"