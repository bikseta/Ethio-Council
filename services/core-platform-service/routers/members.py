from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from models import Member, User
from schemas import MemberCreate, MemberOut
from auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[MemberOut])
def list_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    church_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Member)
    if church_id:
        query = query.filter(Member.church_id == church_id)
    if status:
        query = query.filter(Member.status == status)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(request: MemberCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = Member(**request.model_dump(exclude={"latitude", "longitude"}))
    if request.latitude and request.longitude:
        from geoalchemy2.shape import from_shape
        from shapely.geometry import Point
        member.location = from_shape(Point(request.longitude, request.latitude), srid=4326)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    db.delete(member)
    db.commit()
