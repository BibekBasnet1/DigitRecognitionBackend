from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.userProviders import crud, schemas
from src.core.config import get_db

router = APIRouter()

@router.post("/user_providers/", response_model=schemas.UserProviderInDB)
def create_user_provider(user_provider: schemas.UserProviderCreate, db: Session = Depends(get_db)):
    return crud.create_user_provider(db, user_provider)

@router.get("/user_providers/{user_provider_id}", response_model=schemas.UserProviderInDB)
def read_user_provider(user_provider_id: int, db: Session = Depends(get_db)):
    db_user_provider = crud.get_user_provider(db, user_provider_id)
    if db_user_provider is None:
        raise HTTPException(status_code=404, detail="UserProvider not found")
    return db_user_provider

@router.get("/user_providers/", response_model=List[schemas.UserProviderInDB])
def read_user_providers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_user_providers(db, skip=skip, limit=limit)

@router.put("/user_providers/{user_provider_id}", response_model=schemas.UserProviderInDB)
def update_user_provider(user_provider_id: int, user_provider: schemas.UserProviderCreate, db: Session = Depends(get_db)):
    db_user_provider = crud.update_user_provider(db, user_provider_id, user_provider)
    if db_user_provider is None:
        raise HTTPException(status_code=404, detail="UserProvider not found")
    return db_user_provider

@router.delete("/user_providers/{user_provider_id}", response_model=schemas.UserProviderInDB)
def delete_user_provider(user_provider_id: int, db: Session = Depends(get_db)):
    db_user_provider = crud.delete_user_provider(db, user_provider_id)
    if db_user_provider is None:
        raise HTTPException(status_code=404, detail="UserProvider not found")
    return db_user_provider
