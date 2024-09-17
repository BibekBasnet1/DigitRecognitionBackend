from sqlalchemy.orm import Session
from src.userProviders.models import UserProvider
from src.userProviders.schemas import UserProviderCreate

def create_user_provider(db: Session, user_provider: UserProviderCreate):
    db_user_provider = UserProvider(**user_provider.dict())
    db.add(db_user_provider)
    db.commit()
    db.refresh(db_user_provider)
    return db_user_provider

def get_user_provider(db: Session, user_provider_id: int):
    return db.query(UserProvider).filter(UserProvider.id == user_provider_id).first()

def get_user_providers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserProvider).offset(skip).limit(limit).all()

def update_user_provider(db: Session, user_provider_id: int, user_provider: UserProviderCreate):
    db_user_provider = db.query(UserProvider).filter(UserProvider.id == user_provider_id).first()
    if db_user_provider:
        for var, value in vars(user_provider).items():
            setattr(db_user_provider, var, value) if value else None
        db.commit()
        db.refresh(db_user_provider)
    return db_user_provider

def delete_user_provider(db: Session, user_provider_id: int):
    db_user_provider = db.query(UserProvider).filter(UserProvider.id == user_provider_id).first()
    if db_user_provider:
        db.delete(db_user_provider)
        db.commit()
    return db_user_provider
