from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Denomination, Region
from schemas import UserOut, RegionOut
from auth import get_current_user, require_roles

router = APIRouter()

@router.get("/users", response_model=List[UserOut])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("SUPER_ADMIN", "NATIONAL_ADMIN")),
):
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/regions", response_model=List[RegionOut])
def list_regions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Region).all()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from models import Church, Member, CrisisReport
    return {
        "total_users": db.query(User).count(),
        "total_churches": db.query(Church).count(),
        "total_members": db.query(Member).count(),
        "total_denominations": db.query(Denomination).count(),
        "open_crisis_reports": db.query(CrisisReport).filter(CrisisReport.status == "OPEN").count(),
    }
