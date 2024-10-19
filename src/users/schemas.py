from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    profile_picture: Optional[str] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    email: EmailStr
    password: str  

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True