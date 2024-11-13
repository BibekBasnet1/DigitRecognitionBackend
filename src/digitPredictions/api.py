from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import PredictionBase, PredictionInDB
from src.core.database import get_db
from src.digitPredictions.models import DigitPrediction  

router = APIRouter()

@router.get('/digit_predictions', tags=["digit_predictions"])
def get_digit_predictions(db: Session = Depends(get_db)):
    predictions = db.query(DigitPrediction).all()  
    return {
        "status" : "success",
        "data" : predictions
    }

@router.get('/digit_predictions/{user_id}', tags=["digit_predictions"])
def get_digit_predictions_by_user(user_id: int, db: Session = Depends(get_db)):
    predictions = db.query(DigitPrediction).filter(DigitPrediction.user_id == user_id).all() 
    if not predictions:
        return {
            "status" : "error",
            "message" : "No predictions found for this user",
            "data" : []
        }
    return {
        "status" : "success",
        "data" : predictions
    }  
