from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class IncidentBase(BaseModel):
    title: str
    description: str
    incident_type: str
    severity: str
    status: str = "reported"
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    affected_population: Optional[int] = None
    reported_by: Optional[UUID] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    incident_type: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    affected_population: Optional[int] = None
    reported_by: Optional[UUID] = None


class IncidentRead(IncidentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VolunteerBase(BaseModel):
    user_id: Optional[UUID] = None
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    skills: list[str] = []
    availability: Optional[str] = None
    region_id: Optional[UUID] = None
    is_active: bool = True


class VolunteerCreate(VolunteerBase):
    pass


class VolunteerUpdate(BaseModel):
    user_id: Optional[UUID] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    skills: Optional[list[str]] = None
    availability: Optional[str] = None
    region_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class VolunteerRead(VolunteerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeploymentCreate(BaseModel):
    volunteer_id: UUID
    role: str
    status: str = "assigned"
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ReliefDistributionBase(BaseModel):
    incident_id: UUID
    description: str
    quantity: float
    unit: str
    distribution_date: date
    location: Optional[str] = None
    status: str = "planned"


class ReliefDistributionCreate(ReliefDistributionBase):
    pass


class ReliefDistributionRead(ReliefDistributionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
