from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OAuthProviderBase(BaseModel):
    provider_name: str
    provider_url: str

class OAuthProviderCreate(OAuthProviderBase):
    pass

class OAuthProviderInDB(OAuthProviderBase):
    id: int

    class Config:
        orm_mode = True


