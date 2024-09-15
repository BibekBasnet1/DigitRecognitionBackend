from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProviderBase(BaseModel):
    user_id: int
    provider_id: int
    provider_user_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class UserProviderCreate(UserProviderBase):
    pass

class UserProviderInDB(UserProviderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

