from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Ethio-Council Analytics Service",
    description="Analytics and reporting service for ECFE platform",
    version="1.0.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "healthy", "service": "analytics-service", "version": "1.0.0"}

@app.get("/")
def root():
    return {"message": "Ethio-Council Analytics Service", "docs": "/docs"}

@app.get("/api/v1/analytics/summary")
def get_summary():
    """Platform-wide summary statistics."""
    return {
        "total_members": 0,
        "total_churches": 0,
        "total_denominations": 0,
        "active_crisis_reports": 0,
        "note": "Connect to database for real data",
    }

@app.get("/api/v1/analytics/growth")
def get_growth(period: str = "monthly"):
    """Member and church growth analytics."""
    return {"period": period, "data": [], "note": "Connect to database for real data"}

@app.get("/api/v1/analytics/denominations")
def denomination_stats():
    """Per-denomination statistics."""
    return {"denominations": [], "note": "Connect to database for real data"}

@app.get("/api/v1/analytics/regions")
def region_stats():
    """Per-region statistics."""
    return {"regions": [], "note": "Connect to database for real data"}
