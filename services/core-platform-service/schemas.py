from __future__ import annotations
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# Auth
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_role: str
    user_id: str
    full_name: str

# User
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    denomination_id: Optional[UUID] = None
    region_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes = True

# Denomination
class DenominationOut(BaseModel):
    id: UUID
    name: str
    name_am: Optional[str] = None
    abbreviation: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters_city: Optional[str] = None
    is_active: bool
    class Config:
        from_attributes = True

# Region
class RegionOut(BaseModel):
    id: UUID
    name: str
    name_am: Optional[str] = None
    code: Optional[str] = None
    class Config:
        from_attributes = True

# Church
class ChurchBase(BaseModel):
    denomination_id: UUID
    name: str
    name_am: Optional[str] = None
    pastor_name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    member_count: int = 0
    established_year: Optional[int] = None

class ChurchCreate(ChurchBase):
    woreda_id: Optional[UUID] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ChurchOut(ChurchBase):
    id: UUID
    woreda_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# Member
class MemberBase(BaseModel):
    church_id: UUID
    full_name: str
    full_name_am: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: str = "ACTIVE"

class MemberCreate(MemberBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    baptism_date: Optional[date] = None

class MemberOut(MemberBase):
    id: UUID
    denomination_id: Optional[UUID] = None
    membership_date: Optional[date] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Crisis Report
class CrisisReportBase(BaseModel):
    title: str
    description: str
    severity: str = "MEDIUM"
    church_id: Optional[UUID] = None
    region_id: Optional[UUID] = None
    affected_count: int = 0

class CrisisReportCreate(CrisisReportBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CrisisReportOut(CrisisReportBase):
    id: UUID
    status: str
    reporter_id: Optional[UUID] = None
    response_notes: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime
    class Config:
        from_attributes = True

# Pagination
class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: list
