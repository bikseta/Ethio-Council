from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import DiasporaCommunity, DiasporaPartnership, User
from schemas import (
    DiasporaCommunityCreate,
    DiasporaCommunityResponse,
    DiasporaPartnershipCreate,
    DiasporaPartnershipResponse,
)

router = APIRouter()


def serialize_community(community: DiasporaCommunity) -> DiasporaCommunityResponse:
    return DiasporaCommunityResponse(
        id=community.id,
        name=community.name,
        country=community.country,
        city=community.city,
        contact_person=community.contact_person,
        contact_email=community.contact_email,
        contact_phone=community.contact_phone,
        member_count=community.member_count,
        is_active=community.is_active,
        partnerships_count=len(community.partnerships or []),
        created_at=community.created_at,
    )


def serialize_partnership(partnership: DiasporaPartnership) -> DiasporaPartnershipResponse:
    return DiasporaPartnershipResponse(
        id=partnership.id,
        community_id=partnership.community_id,
        church_id=partnership.church_id,
        partnership_type=partnership.partnership_type,
        description=partnership.description,
        community_name=partnership.community.name if partnership.community else None,
        church_name=partnership.church.name if partnership.church else None,
        is_active=partnership.is_active,
        created_at=partnership.created_at,
    )


@router.get("/communities", response_model=List[DiasporaCommunityResponse])
def list_communities(country: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(DiasporaCommunity).options(selectinload(DiasporaCommunity.partnerships))
    if country:
        query = query.filter(DiasporaCommunity.country.ilike(f"%{country}%"))
    return [serialize_community(item) for item in query.order_by(DiasporaCommunity.name).all()]


@router.get("/communities/{community_id}", response_model=DiasporaCommunityResponse)
def get_community(community_id: int, db: Session = Depends(get_db)):
    community = (
        db.query(DiasporaCommunity)
        .options(selectinload(DiasporaCommunity.partnerships))
        .filter(DiasporaCommunity.id == community_id)
        .first()
    )
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return serialize_community(community)


@router.post("/communities", response_model=DiasporaCommunityResponse, status_code=status.HTTP_201_CREATED)
def create_community(
    community_in: DiasporaCommunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    community = DiasporaCommunity(**community_in.model_dump())
    db.add(community)
    db.commit()
    db.refresh(community)
    db.refresh(current_user)
    return get_community(community.id, db)


@router.get("/partnerships", response_model=List[DiasporaPartnershipResponse])
def list_partnerships(church_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(DiasporaPartnership).options(
        selectinload(DiasporaPartnership.community),
        selectinload(DiasporaPartnership.church),
    )
    if church_id is not None:
        query = query.filter(DiasporaPartnership.church_id == church_id)
    return [serialize_partnership(item) for item in query.order_by(DiasporaPartnership.id.desc()).all()]


@router.post("/partnerships", response_model=DiasporaPartnershipResponse, status_code=status.HTTP_201_CREATED)
def create_partnership(
    partnership_in: DiasporaPartnershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    partnership = DiasporaPartnership(**partnership_in.model_dump())
    db.add(partnership)
    db.commit()
    db.refresh(partnership)
    db.refresh(current_user)
    return serialize_partnership(
        db.query(DiasporaPartnership)
        .options(selectinload(DiasporaPartnership.community), selectinload(DiasporaPartnership.church))
        .filter(DiasporaPartnership.id == partnership.id)
        .first()
    )
