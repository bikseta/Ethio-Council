from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from schemas import ChurchStats, DashboardSummary, DenominationStats, IncidentStats, RegionStats

app = FastAPI(title="ECFE Analytics Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "analytics-service"}


@app.get("/api/v1/analytics/churches", response_model=ChurchStats)
def church_stats(db: Session = Depends(get_db)):
    result = db.execute(text(
        """
        SELECT
            COUNT(*) AS total_churches,
            COALESCE(SUM(member_count), 0) AS total_members,
            COUNT(*) FILTER (WHERE is_active = TRUE) AS active_churches,
            (SELECT COUNT(*) FROM denominations) AS denominations_count
        FROM churches
        """
    )).fetchone()
    return ChurchStats(
        total_churches=result[0],
        total_members=result[1],
        active_churches=result[2],
        denominations_count=result[3],
    )


@app.get("/api/v1/analytics/regions", response_model=List[RegionStats])
def region_stats(db: Session = Depends(get_db)):
    results = db.execute(text(
        """
        SELECT
            r.name,
            COUNT(c.id) AS church_count,
            COALESCE(SUM(c.member_count), 0) AS member_count
        FROM regions r
        LEFT JOIN zones z ON z.region_id = r.id
        LEFT JOIN woredas w ON w.zone_id = z.id
        LEFT JOIN churches c ON c.woreda_id = w.id
        GROUP BY r.id, r.name
        ORDER BY church_count DESC, r.name ASC
        """
    )).fetchall()
    return [RegionStats(region_name=row[0], church_count=row[1], member_count=row[2]) for row in results]


@app.get("/api/v1/analytics/denominations", response_model=List[DenominationStats])
def denomination_stats(db: Session = Depends(get_db)):
    results = db.execute(text(
        """
        SELECT
            d.name,
            COUNT(c.id) AS church_count,
            COALESCE(SUM(c.member_count), 0) AS member_count
        FROM denominations d
        LEFT JOIN churches c ON c.denomination_id = d.id
        GROUP BY d.id, d.name
        ORDER BY church_count DESC, d.name ASC
        """
    )).fetchall()
    return [DenominationStats(denomination_name=row[0], church_count=row[1], member_count=row[2]) for row in results]


@app.get("/api/v1/analytics/dashboard", response_model=DashboardSummary)
def dashboard(db: Session = Depends(get_db)):
    church_summary = church_stats(db)
    top_regions = region_stats(db)
    denomination_breakdown = denomination_stats(db)
    incident_row = db.execute(text(
        """
        SELECT
            COUNT(*) AS total_incidents,
            COUNT(*) FILTER (WHERE status IN ('REPORTED', 'ACTIVE', 'CONTAINED')) AS active_incidents,
            COUNT(*) FILTER (WHERE status = 'RESOLVED') AS resolved_incidents,
            (SELECT COUNT(*) FROM volunteers) AS total_volunteers
        FROM incidents
        """
    )).fetchone()

    incident_stats = IncidentStats(
        total_incidents=incident_row[0],
        active_incidents=incident_row[1],
        resolved_incidents=incident_row[2],
        total_volunteers=incident_row[3],
    )

    return DashboardSummary(
        church_stats=church_summary,
        top_regions=top_regions[:5],
        denomination_breakdown=denomination_breakdown,
        incident_stats=incident_stats,
    )
