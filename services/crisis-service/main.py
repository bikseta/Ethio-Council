from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from datetime import datetime

app = FastAPI(
    title="Ethio-Council Crisis Service",
    description="Crisis and emergency management service for ECFE platform",
    version="1.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CrisisAlert(BaseModel):
    title: str
    description: str
    severity: str = "MEDIUM"
    region_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    affected_count: int = 0

@app.get("/health")
def health():
    return {"status": "healthy", "service": "crisis-service", "version": "1.0.0"}

@app.get("/")
def root():
    return {"message": "Ethio-Council Crisis Service", "docs": "/docs"}

@app.get("/api/v1/crisis/alerts")
def list_alerts(severity: Optional[str] = None, active_only: bool = True):
    """List crisis alerts."""
    return {"alerts": [], "total": 0, "note": "Connect to database for real data"}

@app.post("/api/v1/crisis/alerts", status_code=status.HTTP_201_CREATED)
def create_alert(alert: CrisisAlert):
    """Submit a new crisis alert."""
    return {"id": "placeholder-uuid", "created_at": datetime.utcnow().isoformat(), **alert.model_dump()}

@app.get("/api/v1/crisis/alerts/{alert_id}")
def get_alert(alert_id: str):
    """Get a specific crisis alert."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found (placeholder)")

@app.patch("/api/v1/crisis/alerts/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: str):
    return {"id": alert_id, "status": "ACKNOWLEDGED", "acknowledged_at": datetime.utcnow().isoformat()}

@app.get("/api/v1/crisis/dashboard")
def crisis_dashboard():
    return {
        "open": 0,
        "acknowledged": 0,
        "responding": 0,
        "resolved": 0,
        "critical": 0,
        "note": "Connect to database for real data",
    }
