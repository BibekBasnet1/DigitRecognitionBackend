from fastapi import APIRouter, Depends, HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.users.crud import create_user, get_user_by_email, get_all_users
from src.users.schemas import UserCreate, UserInDB
from src.training.load_model import load_trained_model
from src.training.predict import preprocess_image
import torch
import os

router = APIRouter()

@router.get("/users", response_model=list[UserInDB])
def list_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.post("/users/", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/users/{email}", response_model=UserInDB)
def read_user(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

model = load_trained_model()

@router.post("/users/predict-digit/")
def predict_digit(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        with open(file_location, "wb+") as f:
            f.write(file.file.read())

        image = preprocess_image(file_location)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        image = image.to(device)
        
        with torch.no_grad():
            output = model(image)
            _, predicted = torch.max(output, 1)

        return {"predicted_digit": predicted.item()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
