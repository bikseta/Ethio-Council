from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import Denomination, User
from schemas import DenominationCreate, DenominationResponse

router = APIRouter()


def serialize_denomination(denomination: Denomination) -> DenominationResponse:
    return DenominationResponse(
        id=denomination.id,
        name=denomination.name,
        code=denomination.code,
        founded_year=denomination.founded_year,
        description=denomination.description,
        churches_count=len(denomination.churches or []),
        created_at=denomination.created_at,
    )


@router.get("/", response_model=List[DenominationResponse])
def list_denominations(db: Session = Depends(get_db)):
    denominations = db.query(Denomination).options(selectinload(Denomination.churches)).order_by(Denomination.name).all()
    return [serialize_denomination(item) for item in denominations]


@router.get("/{denomination_id}", response_model=DenominationResponse)
def get_denomination(denomination_id: int, db: Session = Depends(get_db)):
    denomination = (
        db.query(Denomination)
        .options(selectinload(Denomination.churches))
        .filter(Denomination.id == denomination_id)
        .first()
    )
    if not denomination:
        raise HTTPException(status_code=404, detail="Denomination not found")
    return serialize_denomination(denomination)


@router.post("/", response_model=DenominationResponse, status_code=status.HTTP_201_CREATED)
def create_denomination(
    denomination_in: DenominationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    denomination = Denomination(**denomination_in.model_dump())
    db.add(denomination)
    db.commit()
    db.refresh(denomination)
    db.refresh(current_user)
    return get_denomination(denomination.id, db)


@router.put("/{denomination_id}", response_model=DenominationResponse)
def update_denomination(
    denomination_id: int,
    denomination_in: DenominationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    denomination = db.query(Denomination).filter(Denomination.id == denomination_id).first()
    if not denomination:
        raise HTTPException(status_code=404, detail="Denomination not found")
    for field, value in denomination_in.model_dump().items():
        setattr(denomination, field, value)
    db.commit()
    db.refresh(denomination)
    db.refresh(current_user)
    return get_denomination(denomination.id, db)
