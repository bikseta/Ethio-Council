from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FieldRegistrationCreate(BaseModel):
    church_id: UUID
    field_officer_id: UUID
    gps_lat: float
    gps_lng: float
    gps_accuracy: Optional[float] = None
    device_metadata: dict = {}
    notes: Optional[str] = None


class PhotoUploadRequest(BaseModel):
    photo_url: str
    caption: Optional[str] = None


class FieldRegistrationRead(BaseModel):
    id: UUID
    church_id: UUID
    field_officer_id: UUID
    gps_lat: float
    gps_lng: float
    gps_accuracy: Optional[float] = None
    gps_timestamp: datetime
    device_metadata: dict
    photos: list
    registration_status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
