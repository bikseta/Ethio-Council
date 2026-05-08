from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from database import Base, engine, get_db
from models import FieldRegistration
from schemas import FieldRegistrationCreate, FieldRegistrationRead, PhotoUploadRequest


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ethio-Council GIS Registration Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "gis-registration-service"}


@app.post("/registrations", response_model=FieldRegistrationRead, status_code=status.HTTP_201_CREATED)
def create_registration(payload: FieldRegistrationCreate, db: Session = Depends(get_db)):
    registration = FieldRegistration(**payload.model_dump())
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


@app.get("/registrations", response_model=list[FieldRegistrationRead])
def list_registrations(db: Session = Depends(get_db)):
    return db.query(FieldRegistration).order_by(FieldRegistration.created_at.desc()).all()


@app.get("/registrations/{registration_id}", response_model=FieldRegistrationRead)
def get_registration(registration_id, db: Session = Depends(get_db)):
    registration = db.get(FieldRegistration, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


@app.post("/registrations/{registration_id}/photos")
def upload_photo(registration_id, payload: PhotoUploadRequest, db: Session = Depends(get_db)):
    registration = db.get(FieldRegistration, registration_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    photos = list(registration.photos or [])
    photos.append(payload.model_dump())
    registration.photos = photos
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return {"id": str(registration.id), "photos": registration.photos}


@app.get("/map/churches")
def map_churches(db: Session = Depends(get_db)):
    rows = db.execute(text('''
        SELECT id, name, COALESCE(address, '') AS address, verification_status
        FROM churches
        ORDER BY created_at DESC
        LIMIT 500
    ''')).mappings().all()
    return {"type": "FeatureCollection", "features": [
        {
            "type": "Feature",
            "properties": {
                "id": str(row["id"]),
                "name": row["name"],
                "address": row["address"],
                "verification_status": row["verification_status"],
            },
            "geometry": None,
        }
        for row in rows
    ]}


@app.get("/map/heatmap")
def heatmap(db: Session = Depends(get_db)):
    rows = db.execute(text('''
        SELECT region_id, COUNT(*) AS church_count
        FROM churches
        GROUP BY region_id
    ''')).mappings().all()
    return {"data": [dict(row) for row in rows]}
