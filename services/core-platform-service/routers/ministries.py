from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import Ministry, User
from schemas import MinistryCreate, MinistryResponse

router = APIRouter()


def serialize_ministry(ministry: Ministry) -> MinistryResponse:
    return MinistryResponse(
        id=ministry.id,
        name=ministry.name,
        description=ministry.description,
        church_id=ministry.church_id,
        leader_name=ministry.leader_name,
        church_name=ministry.church.name if ministry.church else None,
        created_at=ministry.created_at,
    )


@router.get("/", response_model=List[MinistryResponse])
def list_ministries(church_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Ministry).options(selectinload(Ministry.church))
    if church_id is not None:
        query = query.filter(Ministry.church_id == church_id)
    return [serialize_ministry(item) for item in query.order_by(Ministry.name).all()]


@router.get("/{ministry_id}", response_model=MinistryResponse)
def get_ministry(ministry_id: int, db: Session = Depends(get_db)):
    ministry = db.query(Ministry).options(selectinload(Ministry.church)).filter(Ministry.id == ministry_id).first()
    if not ministry:
        raise HTTPException(status_code=404, detail="Ministry not found")
    return serialize_ministry(ministry)


@router.post("/", response_model=MinistryResponse, status_code=status.HTTP_201_CREATED)
def create_ministry(
    ministry_in: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ministry = Ministry(**ministry_in.model_dump())
    db.add(ministry)
    db.commit()
    db.refresh(ministry)
    db.refresh(current_user)
    return get_ministry(ministry.id, db)


@router.put("/{ministry_id}", response_model=MinistryResponse)
def update_ministry(
    ministry_id: int,
    ministry_in: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ministry = db.query(Ministry).filter(Ministry.id == ministry_id).first()
    if not ministry:
        raise HTTPException(status_code=404, detail="Ministry not found")
    for field, value in ministry_in.model_dump().items():
        setattr(ministry, field, value)
    db.commit()
    db.refresh(ministry)
    db.refresh(current_user)
    return get_ministry(ministry.id, db)
