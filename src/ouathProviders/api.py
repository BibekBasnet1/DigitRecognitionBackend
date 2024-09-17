from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.core.config import get_db
from src.ouathProviders.models import OAuthProvider
from src.ouathProviders.schemas import OAuthProviderCreate, OAuthProviderResponse

router = APIRouter()

@router.post("/oauth-providers/", response_model=OAuthProviderResponse)
def create_oauth_provider(
    oauth_provider: OAuthProviderCreate, db: Session = Depends(get_db)
):
    db_oauth_provider = OAuthProvider(**oauth_provider.dict())
    db.add(db_oauth_provider)
    db.commit()
    db.refresh(db_oauth_provider)
    return db_oauth_provider

@router.get("/oauth-providers/{provider_id}", response_model=OAuthProviderResponse)
def read_oauth_provider(provider_id: int, db: Session = Depends(get_db)):
    db_oauth_provider = db.query(OAuthProvider).filter(OAuthProvider.id == provider_id).first()
    if db_oauth_provider is None:
        raise HTTPException(status_code=404, detail="OAuthProvider not found")
    return db_oauth_provider

@router.get("/oauth-providers/", response_model=list[OAuthProviderResponse])
def read_oauth_providers(db: Session = Depends(get_db)):
    return db.query(OAuthProvider).all()

@router.put("/oauth-providers/{provider_id}", response_model=OAuthProviderResponse)
def update_oauth_provider(
    provider_id: int, oauth_provider: OAuthProviderCreate, db: Session = Depends(get_db)
):
    db_oauth_provider = db.query(OAuthProvider).filter(OAuthProvider.id == provider_id).first()
    if db_oauth_provider is None:
        raise HTTPException(status_code=404, detail="OAuthProvider not found")

    for key, value in oauth_provider.dict().items():
        setattr(db_oauth_provider, key, value)

    db.commit()
    db.refresh(db_oauth_provider)
    return db_oauth_provider

@router.delete("/oauth-providers/{provider_id}", response_model=OAuthProviderResponse)
def delete_oauth_provider(provider_id: int, db: Session = Depends(get_db)):
    db_oauth_provider = db.query(OAuthProvider).filter(OAuthProvider.id == provider_id).first()
    if db_oauth_provider is None:
        raise HTTPException(status_code=404, detail="OAuthProvider not found")

    db.delete(db_oauth_provider)
    db.commit()
    return db_oauth_provider
