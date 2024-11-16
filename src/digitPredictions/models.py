from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from src.core.config import Base
# from src.users.models import User

class DigitPrediction(Base):
    __tablename__ = "digit_predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  
    uploaded_image = Column(String)  
    predicted_digit = Column(Integer)  
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Integer, default=0)

    user = relationship("User", back_populates="predictions")
