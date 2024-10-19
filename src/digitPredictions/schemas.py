from pydantic import BaseModel
from datetime import datetime


class PredictionBase(BaseModel):
    user_id: int
    uploaded_img: str
    predicted_digit: int
    confidence: float
    created_at : datetime
    status : int # 0: pending, 1: completed, 2: failed


class PredictionInDB(PredictionBase):
    id: int
    created_at: datetime
    status: int

    class Config:
        orm_mode = True

