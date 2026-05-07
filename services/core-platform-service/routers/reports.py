from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database import get_db
from models import CrisisReport, User
from schemas import CrisisReportCreate, CrisisReportOut
from auth import get_current_user

router = APIRouter()

@router.get("/crisis", response_model=List[CrisisReportOut])
def list_crisis_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    severity: Optional[str] = None,
    report_status: Optional[str] = None,
    region_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(CrisisReport)
    if severity:
        query = query.filter(CrisisReport.severity == severity)
    if report_status:
        query = query.filter(CrisisReport.status == report_status)
    if region_id:
        query = query.filter(CrisisReport.region_id == region_id)
    return query.order_by(CrisisReport.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/crisis", response_model=CrisisReportOut, status_code=status.HTTP_201_CREATED)
def create_crisis_report(
    request: CrisisReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = CrisisReport(**request.model_dump(exclude={"latitude", "longitude"}), reporter_id=current_user.id)
    if request.latitude and request.longitude:
        from geoalchemy2.shape import from_shape
        from shapely.geometry import Point
        report.location = from_shape(Point(request.longitude, request.latitude), srid=4326)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

@router.patch("/crisis/{report_id}/status")
def update_crisis_status(
    report_id: UUID,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = db.query(CrisisReport).filter(CrisisReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    report.status = new_status
    db.commit()
    return {"id": str(report_id), "status": new_status}
