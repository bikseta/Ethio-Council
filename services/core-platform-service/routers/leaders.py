from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import ChurchLeader, User
from schemas import LeaderCreate, LeaderRead, LeaderUpdate


router = APIRouter(prefix="/leaders", tags=["leaders"])


@router.get("", response_model=list[LeaderRead])
def list_leaders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(ChurchLeader).order_by(ChurchLeader.created_at.desc()).all()


@router.post("", response_model=LeaderRead, status_code=status.HTTP_201_CREATED)
def create_leader(payload: LeaderCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    leader = ChurchLeader(**payload.model_dump())
    db.add(leader)
    db.commit()
    db.refresh(leader)
    return leader


@router.get("/{leader_id}", response_model=LeaderRead)
def get_leader(leader_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    leader = db.get(ChurchLeader, leader_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    return leader


@router.put("/{leader_id}", response_model=LeaderRead)
def update_leader(leader_id: UUID, payload: LeaderUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    leader = db.get(ChurchLeader, leader_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(leader, field, value)
    db.add(leader)
    db.commit()
    db.refresh(leader)
    return leader


@router.delete("/{leader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leader(leader_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    leader = db.get(ChurchLeader, leader_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Leader not found")
    db.delete(leader)
    db.commit()
