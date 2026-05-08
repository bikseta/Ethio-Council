from typing import List, Optional
from pydantic import BaseModel


class ChurchStats(BaseModel):
    total_churches: int
    total_members: int
    active_churches: int
    denominations_count: int


class RegionStats(BaseModel):
    region_name: str
    church_count: int
    member_count: int


class DenominationStats(BaseModel):
    denomination_name: str
    church_count: int
    member_count: int


class IncidentStats(BaseModel):
    total_incidents: int
    active_incidents: int
    resolved_incidents: int
    total_volunteers: int


class DashboardSummary(BaseModel):
    church_stats: ChurchStats
    top_regions: List[RegionStats]
    denomination_breakdown: List[DenominationStats]
    incident_stats: Optional[IncidentStats] = None
