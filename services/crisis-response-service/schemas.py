from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models import IncidentSeverity, IncidentStatus, VolunteerStatus


class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    reported_by: int
    woreda_id: Optional[int] = None
    affected_count: int = 0


class IncidentCreate(IncidentBase):
    pass


class IncidentResponse(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class VolunteerBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    skills: Optional[str] = None
    church_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VolunteerCreate(VolunteerBase):
    pass


class VolunteerResponse(VolunteerBase):
    id: int
    status: VolunteerStatus
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ReliefDistributionBase(BaseModel):
    incident_id: int
    item_name: str
    quantity: float
    unit: Optional[str] = None
    distributed_to: Optional[str] = None
    distributed_by: Optional[int] = None
    notes: Optional[str] = None


class ReliefDistributionCreate(ReliefDistributionBase):
    pass


class ReliefDistributionResponse(ReliefDistributionBase):
    id: int
    distributed_at: datetime

    class Config:
        from_attributes = True
