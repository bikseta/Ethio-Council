from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Church, User
from schemas import ChurchCreate, ChurchRead, ChurchUpdate, VerifyChurchResponse


router = APIRouter(prefix="/churches", tags=["churches"])


@router.get("", response_model=list[ChurchRead])
def list_churches(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Church).order_by(Church.created_at.desc()).all()


@router.post("", response_model=ChurchRead, status_code=status.HTTP_201_CREATED)
def create_church(payload: ChurchCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    church = Church(**payload.model_dump())
    db.add(church)
    db.commit()
    db.refresh(church)
    return church


@router.get("/{church_id}", response_model=ChurchRead)
def get_church(church_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    church = db.get(Church, church_id)
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    return church


@router.put("/{church_id}", response_model=ChurchRead)
def update_church(church_id: UUID, payload: ChurchUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    church = db.get(Church, church_id)
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(church, field, value)
    db.add(church)
    db.commit()
    db.refresh(church)
    return church


@router.delete("/{church_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_church(church_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    church = db.get(Church, church_id)
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    db.delete(church)
    db.commit()


@router.post("/{church_id}/verify", response_model=VerifyChurchResponse)
def verify_church(church_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    church = db.get(Church, church_id)
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    church.is_verified = True
    church.verification_status = "verified"
    db.add(church)
    db.commit()
    db.refresh(church)
    return VerifyChurchResponse(id=church.id, verification_status="verified", is_verified=True)
