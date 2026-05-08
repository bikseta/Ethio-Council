from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from models import FieldRegistration
from schemas import FieldRegistrationCreate, FieldRegistrationResponse

app = FastAPI(title="ECFE GIS Registration Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "gis-registration-service"}


@app.get("/api/v1/summary")
def registration_summary(db: Session = Depends(get_db)):
    return {
        "registrations": db.query(FieldRegistration).count(),
        "verified": db.query(FieldRegistration).filter(FieldRegistration.status == "VERIFIED").count(),
        "pending": db.query(FieldRegistration).filter(FieldRegistration.status == "PENDING").count(),
    }


@app.get("/api/v1/registrations", response_model=List[FieldRegistrationResponse])
def list_registrations(status_filter: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(FieldRegistration)
    if status_filter:
        query = query.filter(FieldRegistration.status == status_filter.upper())
    return query.order_by(FieldRegistration.created_at.desc()).all()


@app.get("/api/v1/registrations/{reg_id}", response_model=FieldRegistrationResponse)
def get_registration(reg_id: int, db: Session = Depends(get_db)):
    registration = db.query(FieldRegistration).filter(FieldRegistration.id == reg_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


@app.post("/api/v1/registrations", response_model=FieldRegistrationResponse, status_code=status.HTTP_201_CREATED)
def create_registration(registration_in: FieldRegistrationCreate, db: Session = Depends(get_db)):
    registration = FieldRegistration(**registration_in.model_dump())
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration
