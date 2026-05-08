from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RegionBase(BaseModel):
    name: str
    code: str


class RegionCreate(RegionBase):
    pass


class RegionResponse(RegionBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ZoneBase(BaseModel):
    name: str
    code: str
    region_id: int


class ZoneCreate(ZoneBase):
    pass


class ZoneResponse(ZoneBase):
    id: int
    region_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WoredaBase(BaseModel):
    name: str
    code: str
    zone_id: int


class WoredaCreate(WoredaBase):
    pass


class WoredaResponse(WoredaBase):
    id: int
    zone_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KebeleBase(BaseModel):
    name: str
    code: str
    woreda_id: int


class KebeleCreate(KebeleBase):
    pass


class KebeleResponse(KebeleBase):
    id: int
    woreda_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DenominationBase(BaseModel):
    name: str
    code: str
    founded_year: Optional[int] = None
    description: Optional[str] = None


class DenominationCreate(DenominationBase):
    pass


class DenominationResponse(DenominationBase):
    id: int
    churches_count: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChurchBase(BaseModel):
    name: str
    denomination_id: int
    woreda_id: int
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    established_year: Optional[int] = None
    member_count: int = 0
    is_active: bool = True


class ChurchCreate(ChurchBase):
    pass


class ChurchResponse(ChurchBase):
    id: int
    denomination_name: Optional[str] = None
    woreda_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MinistryBase(BaseModel):
    name: str
    description: Optional[str] = None
    church_id: int
    leader_name: Optional[str] = None


class MinistryCreate(MinistryBase):
    pass


class MinistryResponse(MinistryBase):
    id: int
    church_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ChurchLeaderBase(BaseModel):
    full_name: str
    title: Optional[str] = None
    church_id: int
    phone: Optional[str] = None
    email: Optional[str] = None
    ordained_year: Optional[int] = None
    is_active: bool = True


class ChurchLeaderCreate(ChurchLeaderBase):
    pass


class ChurchLeaderResponse(ChurchLeaderBase):
    id: int
    church_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiasporaCommunityBase(BaseModel):
    name: str
    country: str
    city: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    member_count: int = 0
    is_active: bool = True


class DiasporaCommunityCreate(DiasporaCommunityBase):
    pass


class DiasporaCommunityResponse(DiasporaCommunityBase):
    id: int
    partnerships_count: Optional[int] = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiasporaPartnershipBase(BaseModel):
    community_id: int
    church_id: int
    partnership_type: Optional[str] = None
    description: Optional[str] = None


class DiasporaPartnershipCreate(DiasporaPartnershipBase):
    pass


class DiasporaPartnershipResponse(DiasporaPartnershipBase):
    id: int
    community_name: Optional[str] = None
    church_name: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HierarchySummary(BaseModel):
    regions: int
    zones: int
    woredas: int
    kebeles: int
