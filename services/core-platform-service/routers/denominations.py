from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Denomination, User
from schemas import DenominationCreate, DenominationRead, DenominationUpdate


router = APIRouter(prefix="/denominations", tags=["denominations"])


@router.get("", response_model=list[DenominationRead])
def list_denominations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Denomination).order_by(Denomination.name.asc()).all()


@router.post("", response_model=DenominationRead, status_code=status.HTTP_201_CREATED)
def create_denomination(payload: DenominationCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    denomination = Denomination(**payload.model_dump())
    db.add(denomination)
    db.commit()
    db.refresh(denomination)
    return denomination


@router.get("/{denomination_id}", response_model=DenominationRead)
def get_denomination(denomination_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    denomination = db.get(Denomination, denomination_id)
    if not denomination:
        raise HTTPException(status_code=404, detail="Denomination not found")
    return denomination


@router.put("/{denomination_id}", response_model=DenominationRead)
def update_denomination(denomination_id: UUID, payload: DenominationUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    denomination = db.get(Denomination, denomination_id)
    if not denomination:
        raise HTTPException(status_code=404, detail="Denomination not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(denomination, field, value)
    db.add(denomination)
    db.commit()
    db.refresh(denomination)
    return denomination


@router.delete("/{denomination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_denomination(denomination_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    denomination = db.get(Denomination, denomination_id)
    if not denomination:
        raise HTTPException(status_code=404, detail="Denomination not found")
    db.delete(denomination)
    db.commit()
