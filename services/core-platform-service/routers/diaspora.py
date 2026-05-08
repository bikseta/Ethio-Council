from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import DiasporaCommunity, DiasporaPartnership, User
from schemas import (
    DiasporaCommunityCreate,
    DiasporaCommunityRead,
    DiasporaCommunityUpdate,
    DiasporaPartnershipCreate,
    DiasporaPartnershipRead,
)


router = APIRouter(prefix="/diaspora", tags=["diaspora"])


@router.get("/communities", response_model=list[DiasporaCommunityRead])
def list_communities(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(DiasporaCommunity).order_by(DiasporaCommunity.created_at.desc()).all()


@router.post("/communities", response_model=DiasporaCommunityRead, status_code=status.HTTP_201_CREATED)
def create_community(payload: DiasporaCommunityCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    community = DiasporaCommunity(**payload.model_dump())
    db.add(community)
    db.commit()
    db.refresh(community)
    return community


@router.get("/communities/{community_id}", response_model=DiasporaCommunityRead)
def get_community(community_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    community = db.get(DiasporaCommunity, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Diaspora community not found")
    return community


@router.put("/communities/{community_id}", response_model=DiasporaCommunityRead)
def update_community(community_id: UUID, payload: DiasporaCommunityUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    community = db.get(DiasporaCommunity, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Diaspora community not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(community, field, value)
    db.add(community)
    db.commit()
    db.refresh(community)
    return community


@router.delete("/communities/{community_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_community(community_id: UUID, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    community = db.get(DiasporaCommunity, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="Diaspora community not found")
    db.delete(community)
    db.commit()


@router.get("/partnerships", response_model=list[DiasporaPartnershipRead])
def list_partnerships(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(DiasporaPartnership).order_by(DiasporaPartnership.created_at.desc()).all()


@router.post("/partnerships", response_model=DiasporaPartnershipRead, status_code=status.HTTP_201_CREATED)
def create_partnership(payload: DiasporaPartnershipCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    partnership = DiasporaPartnership(**payload.model_dump())
    db.add(partnership)
    db.commit()
    db.refresh(partnership)
    return partnership
