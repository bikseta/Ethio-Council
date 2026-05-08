from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Ministry, User
from schemas import MinistryCreate, MinistryRead, MinistryUpdate


router = APIRouter(prefix="/ministries", tags=["ministries"])


@router.get("", response_model=list[MinistryRead])
def list_ministries(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Ministry).order_by(Ministry.created_at.desc()).all()


@router.post("", response_model=MinistryRead, status_code=status.HTTP_201_CREATED)
def create_ministry(payload: MinistryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ministry = Ministry(**payload.model_dump())
    db.add(ministry)
    db.commit()
    db.refresh(ministry)
    return ministry


@router.get("/{ministry_id}", response_model=MinistryRead)
def get_ministry(ministry_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ministry = db.get(Ministry, ministry_id)
    if not ministry:
        raise HTTPException(status_code=404, detail="Ministry not found")
    return ministry


@router.put("/{ministry_id}", response_model=MinistryRead)
def update_ministry(ministry_id: UUID, payload: MinistryUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ministry = db.get(Ministry, ministry_id)
    if not ministry:
        raise HTTPException(status_code=404, detail="Ministry not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(ministry, field, value)
    db.add(ministry)
    db.commit()
    db.refresh(ministry)
    return ministry


@router.delete("/{ministry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ministry(ministry_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ministry = db.get(Ministry, ministry_id)
    if not ministry:
        raise HTTPException(status_code=404, detail="Ministry not found")
    db.delete(ministry)
    db.commit()
