from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config import settings
from database import Base, engine, get_db
from models import Incident, ReliefDistribution, Volunteer, VolunteerDeployment
from schemas import (
    DeploymentCreate,
    IncidentCreate,
    IncidentRead,
    IncidentUpdate,
    ReliefDistributionCreate,
    ReliefDistributionRead,
    VolunteerCreate,
    VolunteerRead,
    VolunteerUpdate,
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ethio-Council Crisis Response Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "crisis-response-service"}


@app.get("/incidents", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).order_by(Incident.created_at.desc()).all()


@app.post("/incidents", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@app.get("/incidents/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@app.put("/incidents/{incident_id}", response_model=IncidentRead)
def update_incident(incident_id, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@app.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()


@app.get("/volunteers", response_model=list[VolunteerRead])
def list_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).order_by(Volunteer.created_at.desc()).all()


@app.post("/volunteers", response_model=VolunteerRead, status_code=status.HTTP_201_CREATED)
def create_volunteer(payload: VolunteerCreate, db: Session = Depends(get_db)):
    volunteer = Volunteer(**payload.model_dump())
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@app.get("/volunteers/{volunteer_id}", response_model=VolunteerRead)
def get_volunteer(volunteer_id, db: Session = Depends(get_db)):
    volunteer = db.get(Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer


@app.put("/volunteers/{volunteer_id}", response_model=VolunteerRead)
def update_volunteer(volunteer_id, payload: VolunteerUpdate, db: Session = Depends(get_db)):
    volunteer = db.get(Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(volunteer, field, value)
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@app.delete("/volunteers/{volunteer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_volunteer(volunteer_id, db: Session = Depends(get_db)):
    volunteer = db.get(Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    db.delete(volunteer)
    db.commit()


@app.post("/incidents/{incident_id}/volunteers", status_code=status.HTTP_201_CREATED)
def deploy_volunteer(incident_id, payload: DeploymentCreate, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    volunteer = db.get(Volunteer, payload.volunteer_id)
    if not incident or not volunteer:
        raise HTTPException(status_code=404, detail="Incident or volunteer not found")
    deployment = VolunteerDeployment(incident_id=incident.id, volunteer_id=volunteer.id, role=payload.role, status=payload.status, start_date=payload.start_date, end_date=payload.end_date)
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return {"id": str(deployment.id), "incident_id": str(incident.id), "volunteer_id": str(volunteer.id), "status": deployment.status}


@app.get("/relief-distributions", response_model=list[ReliefDistributionRead])
def list_distributions(db: Session = Depends(get_db)):
    return db.query(ReliefDistribution).order_by(ReliefDistribution.created_at.desc()).all()


@app.post("/relief-distributions", response_model=ReliefDistributionRead, status_code=status.HTTP_201_CREATED)
def create_distribution(payload: ReliefDistributionCreate, db: Session = Depends(get_db)):
    distribution = ReliefDistribution(**payload.model_dump())
    db.add(distribution)
    db.commit()
    db.refresh(distribution)
    return distribution
