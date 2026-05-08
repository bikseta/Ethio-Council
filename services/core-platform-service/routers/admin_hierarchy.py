from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Kebele, Region, User, Woreda, Zone


router = APIRouter(prefix="/admin-hierarchy", tags=["admin-hierarchy"])


@router.get("/regions")
def list_regions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Region).order_by(Region.name.asc()).all()


@router.get("/zones")
def list_zones(region_id: UUID | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Zone)
    if region_id:
        query = query.filter(Zone.region_id == region_id)
    return query.order_by(Zone.name.asc()).all()


@router.get("/woredas")
def list_woredas(zone_id: UUID | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Woreda)
    if zone_id:
        query = query.filter(Woreda.zone_id == zone_id)
    return query.order_by(Woreda.name.asc()).all()


@router.get("/kebeles")
def list_kebeles(woreda_id: UUID | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Kebele)
    if woreda_id:
        query = query.filter(Kebele.woreda_id == woreda_id)
    return query.order_by(Kebele.name.asc()).all()
