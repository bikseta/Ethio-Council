from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from models import Church, Denomination, User
from schemas import ChurchCreate, ChurchOut, DenominationOut
from auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ChurchOut])
def list_churches(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    denomination_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Church)
    if denomination_id:
        query = query.filter(Church.denomination_id == denomination_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ChurchOut, status_code=status.HTTP_201_CREATED)
def create_church(request: ChurchCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    church = Church(**request.model_dump(exclude={"latitude", "longitude"}))
    if request.latitude and request.longitude:
        from geoalchemy2.shape import from_shape
        from shapely.geometry import Point
        church.location = from_shape(Point(request.longitude, request.latitude), srid=4326)
    db.add(church)
    db.commit()
    db.refresh(church)
    return church

@router.get("/denominations", response_model=List[DenominationOut])
def list_denominations(db: Session = Depends(get_db)):
    return db.query(Denomination).filter(Denomination.is_active == True).all()

@router.get("/{church_id}", response_model=ChurchOut)
def get_church(church_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    church = db.query(Church).filter(Church.id == church_id).first()
    if not church:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Church not found")
    return church
