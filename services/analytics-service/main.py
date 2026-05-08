from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import settings
from database import get_db


app = FastAPI(title="Ethio-Council Analytics Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "analytics-service"}


@app.get("/dashboard/overview")
def dashboard_overview(db: Session = Depends(get_db)):
    return {
        "total_churches": db.execute(text("SELECT COUNT(*) FROM churches")).scalar() or 0,
        "total_ministries": db.execute(text("SELECT COUNT(*) FROM ministries")).scalar() or 0,
        "total_denominations": db.execute(text("SELECT COUNT(*) FROM denominations")).scalar() or 0,
        "regions_covered": db.execute(text("SELECT COUNT(DISTINCT region_id) FROM churches WHERE region_id IS NOT NULL")).scalar() or 0,
        "active_crises": db.execute(text("SELECT COUNT(*) FROM incidents WHERE status <> 'resolved'")).scalar() or 0,
    }


@app.get("/dashboard/by-region")
def by_region(db: Session = Depends(get_db)):
    rows = db.execute(text('''
        SELECT r.name AS region, COUNT(c.id) AS church_count
        FROM regions r
        LEFT JOIN churches c ON c.region_id = r.id
        GROUP BY r.name
        ORDER BY church_count DESC, r.name ASC
    ''')).mappings().all()
    return [dict(row) for row in rows]


@app.get("/dashboard/by-denomination")
def by_denomination(db: Session = Depends(get_db)):
    rows = db.execute(text('''
        SELECT d.name AS denomination, COUNT(c.id) AS church_count
        FROM denominations d
        LEFT JOIN churches c ON c.denomination_id = d.id
        GROUP BY d.name
        ORDER BY church_count DESC, d.name ASC
    ''')).mappings().all()
    return [dict(row) for row in rows]


@app.get("/dashboard/ministry-types")
def ministry_types(db: Session = Depends(get_db)):
    rows = db.execute(text('''
        SELECT ministry_type, COUNT(*) AS total
        FROM ministries
        GROUP BY ministry_type
        ORDER BY total DESC, ministry_type ASC
    ''')).mappings().all()
    return [dict(row) for row in rows]


@app.get("/reports/summary")
def report_summary(db: Session = Depends(get_db)):
    overview = dashboard_overview(db)
    by_region_data = by_region(db)
    by_denomination_data = by_denomination(db)
    return {
        "generated_for": "ECFE",
        "overview": overview,
        "top_regions": by_region_data[:5],
        "top_denominations": by_denomination_data[:5],
    }
