from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from models import RegistrationStatus


class FieldRegistrationBase(BaseModel):
    church_id: int
    field_officer_id: int
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class FieldRegistrationCreate(FieldRegistrationBase):
    pass


class FieldRegistrationResponse(FieldRegistrationBase):
    id: int
    status: RegistrationStatus
    created_at: datetime

    class Config:
        from_attributes = True


class RegistrationPhotoResponse(BaseModel):
    id: int
    registration_id: int
    s3_key: str
    caption: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
