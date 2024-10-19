from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .schemas import PredictionBase, PredictionInDB 
from src.core.database import get_db

router = APIRouter()

# get all the predictions that exists
@router.get('/digit_predictions')
def get_digit_predictions(digit_predictions: PredictionInDB , db: Session = Depends(get_db)):
    return db.query(digit_predictions).all()

# get predictions based on the users 
@router.get('/digit_predictions/{user_id}')
def get_digit_predictions_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(PredictionInDB).filter(PredictionInDB.user_id == user_id).all()


