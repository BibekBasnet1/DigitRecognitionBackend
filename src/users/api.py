from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.users.crud import create_user, get_user_by_email, get_all_users
from src.users.schemas import UserCreate, UserInDB

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
