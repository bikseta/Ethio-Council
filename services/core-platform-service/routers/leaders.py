from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import ChurchLeader, User
from schemas import ChurchLeaderCreate, ChurchLeaderResponse

router = APIRouter()


def serialize_leader(leader: ChurchLeader) -> ChurchLeaderResponse:
    return ChurchLeaderResponse(
        id=leader.id,
        full_name=leader.full_name,
        title=leader.title,
        church_id=leader.church_id,
        phone=leader.phone,
        email=leader.email,
        ordained_year=leader.ordained_year,
        is_active=leader.is_active,
        church_name=leader.church.name if leader.church else None,
        created_at=leader.created_at,
    )


@router.get("/", response_model=List[ChurchLeaderResponse])
def list_leaders(church_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(ChurchLeader).options(selectinload(ChurchLeader.church))
    if church_id is not None:
        query = query.filter(ChurchLeader.church_id == church_id)
    return [serialize_leader(item) for item in query.order_by(ChurchLeader.full_name).all()]


@router.get("/{leader_id}", response_model=ChurchLeaderResponse)
def get_leader(leader_id: int, db: Session = Depends(get_db)):
    leader = db.query(ChurchLeader).options(selectinload(ChurchLeader.church)).filter(ChurchLeader.id == leader_id).first()
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    return serialize_leader(leader)


@router.post("/", response_model=ChurchLeaderResponse, status_code=status.HTTP_201_CREATED)
def create_leader(
    leader_in: ChurchLeaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leader = ChurchLeader(**leader_in.model_dump())
    db.add(leader)
    db.commit()
    db.refresh(leader)
    db.refresh(current_user)
    return get_leader(leader.id, db)


@router.put("/{leader_id}", response_model=ChurchLeaderResponse)
def update_leader(
    leader_id: int,
    leader_in: ChurchLeaderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leader = db.query(ChurchLeader).filter(ChurchLeader.id == leader_id).first()
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    for field, value in leader_in.model_dump().items():
        setattr(leader, field, value)
    db.commit()
    db.refresh(leader)
    db.refresh(current_user)
    return get_leader(leader.id, db)
