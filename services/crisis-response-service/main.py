from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from models import Incident, ReliefDistribution, Volunteer
from schemas import (
    IncidentCreate,
    IncidentResponse,
    ReliefDistributionCreate,
    ReliefDistributionResponse,
    VolunteerCreate,
    VolunteerResponse,
)

app = FastAPI(title="ECFE Crisis Response Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "crisis-response-service"}


@app.get("/api/v1/summary")
def crisis_summary(db: Session = Depends(get_db)):
    return {
        "incidents": db.query(Incident).count(),
        "active_incidents": db.query(Incident).filter(Incident.status.in_(["REPORTED", "ACTIVE", "CONTAINED"])).count(),
        "volunteers": db.query(Volunteer).count(),
        "available_volunteers": db.query(Volunteer).filter(Volunteer.status == "AVAILABLE").count(),
        "distributions": db.query(ReliefDistribution).count(),
    }


@app.get("/api/v1/incidents", response_model=List[IncidentResponse])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@app.get("/api/v1/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.post("/api/v1/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(incident_in: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**incident_in.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@app.get("/api/v1/volunteers", response_model=List[VolunteerResponse])
def list_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).order_by(Volunteer.created_at.desc()).all()


@app.post("/api/v1/volunteers", response_model=VolunteerResponse, status_code=status.HTTP_201_CREATED)
def create_volunteer(volunteer_in: VolunteerCreate, db: Session = Depends(get_db)):
    volunteer = Volunteer(**volunteer_in.model_dump())
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@app.get("/api/v1/distributions", response_model=List[ReliefDistributionResponse])
def list_distributions(db: Session = Depends(get_db)):
    return db.query(ReliefDistribution).order_by(ReliefDistribution.distributed_at.desc()).all()


@app.post("/api/v1/distributions", response_model=ReliefDistributionResponse, status_code=status.HTTP_201_CREATED)
def create_distribution(distribution_in: ReliefDistributionCreate, db: Session = Depends(get_db)):
    distribution = ReliefDistribution(**distribution_in.model_dump())
    db.add(distribution)
    db.commit()
    db.refresh(distribution)
    return distribution
