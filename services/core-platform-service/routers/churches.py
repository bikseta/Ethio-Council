from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import Church, User
from schemas import ChurchCreate, ChurchResponse

router = APIRouter()


def serialize_church(church: Church) -> ChurchResponse:
    return ChurchResponse(
        id=church.id,
        name=church.name,
        denomination_id=church.denomination_id,
        woreda_id=church.woreda_id,
        address=church.address,
        phone=church.phone,
        email=church.email,
        established_year=church.established_year,
        member_count=church.member_count,
        is_active=church.is_active,
        denomination_name=church.denomination.name if church.denomination else None,
        woreda_name=church.woreda.name if church.woreda else None,
        created_at=church.created_at,
        updated_at=church.updated_at,
    )


@router.get("/", response_model=List[ChurchResponse])
def list_churches(
    denomination_id: Optional[int] = Query(default=None),
    woreda_id: Optional[int] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Church).options(selectinload(Church.denomination), selectinload(Church.woreda))
    if denomination_id is not None:
        query = query.filter(Church.denomination_id == denomination_id)
    if woreda_id is not None:
        query = query.filter(Church.woreda_id == woreda_id)
    if is_active is not None:
        query = query.filter(Church.is_active == is_active)
    return [serialize_church(church) for church in query.order_by(Church.name).all()]


@router.get("/{church_id}", response_model=ChurchResponse)
def get_church(church_id: int, db: Session = Depends(get_db)):
    church = (
        db.query(Church)
        .options(selectinload(Church.denomination), selectinload(Church.woreda))
        .filter(Church.id == church_id)
        .first()
    )
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    return serialize_church(church)


@router.post("/", response_model=ChurchResponse, status_code=status.HTTP_201_CREATED)
def create_church(
    church_in: ChurchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    church = Church(**church_in.model_dump())
    db.add(church)
    db.commit()
    db.refresh(church)
    db.refresh(current_user)
    return get_church(church.id, db)


@router.put("/{church_id}", response_model=ChurchResponse)
def update_church(
    church_id: int,
    church_in: ChurchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    for field, value in church_in.model_dump().items():
        setattr(church, field, value)
    db.commit()
    db.refresh(church)
    db.refresh(current_user)
    return get_church(church.id, db)


@router.delete("/{church_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_church(
    church_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(status_code=404, detail="Church not found")
    db.delete(church)
    db.commit()
    db.refresh(current_user)
