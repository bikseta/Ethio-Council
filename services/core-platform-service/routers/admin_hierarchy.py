from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session, selectinload

from auth import get_current_user
from database import get_db
from models import Kebele, Region, User, Woreda, Zone
from schemas import (
    HierarchySummary,
    KebeleCreate,
    KebeleResponse,
    RegionCreate,
    RegionResponse,
    WoredaCreate,
    WoredaResponse,
    ZoneCreate,
    ZoneResponse,
)

router = APIRouter()


def serialize_zone(zone: Zone) -> ZoneResponse:
    return ZoneResponse(
        id=zone.id,
        name=zone.name,
        code=zone.code,
        region_id=zone.region_id,
        region_name=zone.region.name if zone.region else None,
        created_at=zone.created_at,
    )


def serialize_woreda(woreda: Woreda) -> WoredaResponse:
    return WoredaResponse(
        id=woreda.id,
        name=woreda.name,
        code=woreda.code,
        zone_id=woreda.zone_id,
        zone_name=woreda.zone.name if woreda.zone else None,
        created_at=woreda.created_at,
    )


def serialize_kebele(kebele: Kebele) -> KebeleResponse:
    return KebeleResponse(
        id=kebele.id,
        name=kebele.name,
        code=kebele.code,
        woreda_id=kebele.woreda_id,
        woreda_name=kebele.woreda.name if kebele.woreda else None,
        created_at=kebele.created_at,
    )


@router.get("/summary", response_model=HierarchySummary)
def hierarchy_summary(db: Session = Depends(get_db)):
    return HierarchySummary(
        regions=db.query(Region).count(),
        zones=db.query(Zone).count(),
        woredas=db.query(Woreda).count(),
        kebeles=db.query(Kebele).count(),
    )


@router.get("/regions", response_model=List[RegionResponse])
def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).order_by(Region.name).all()


@router.post("/regions", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
def create_region(region_in: RegionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    region = Region(**region_in.model_dump())
    db.add(region)
    db.commit()
    db.refresh(region)
    db.refresh(current_user)
    return region


@router.get("/zones", response_model=List[ZoneResponse])
def list_zones(region_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Zone).options(selectinload(Zone.region))
    if region_id is not None:
        query = query.filter(Zone.region_id == region_id)
    return [serialize_zone(item) for item in query.order_by(Zone.name).all()]


@router.post("/zones", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
def create_zone(zone_in: ZoneCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    zone = Zone(**zone_in.model_dump())
    db.add(zone)
    db.commit()
    db.refresh(zone)
    db.refresh(current_user)
    return serialize_zone(db.query(Zone).options(selectinload(Zone.region)).filter(Zone.id == zone.id).first())


@router.get("/woredas", response_model=List[WoredaResponse])
def list_woredas(zone_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Woreda).options(selectinload(Woreda.zone))
    if zone_id is not None:
        query = query.filter(Woreda.zone_id == zone_id)
    return [serialize_woreda(item) for item in query.order_by(Woreda.name).all()]


@router.post("/woredas", response_model=WoredaResponse, status_code=status.HTTP_201_CREATED)
def create_woreda(woreda_in: WoredaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    woreda = Woreda(**woreda_in.model_dump())
    db.add(woreda)
    db.commit()
    db.refresh(woreda)
    db.refresh(current_user)
    return serialize_woreda(db.query(Woreda).options(selectinload(Woreda.zone)).filter(Woreda.id == woreda.id).first())


@router.get("/kebeles", response_model=List[KebeleResponse])
def list_kebeles(woreda_id: Optional[int] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Kebele).options(selectinload(Kebele.woreda))
    if woreda_id is not None:
        query = query.filter(Kebele.woreda_id == woreda_id)
    return [serialize_kebele(item) for item in query.order_by(Kebele.name).all()]


@router.post("/kebeles", response_model=KebeleResponse, status_code=status.HTTP_201_CREATED)
def create_kebele(kebele_in: KebeleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    kebele = Kebele(**kebele_in.model_dump())
    db.add(kebele)
    db.commit()
    db.refresh(kebele)
    db.refresh(current_user)
    return serialize_kebele(db.query(Kebele).options(selectinload(Kebele.woreda)).filter(Kebele.id == kebele.id).first())
