from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    token: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8)
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    language_preference: str = "en"
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    kebele_id: Optional[UUID] = None


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool
    language_preference: str
    created_at: datetime
    last_login_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DenominationBase(BaseModel):
    name: str
    abbreviation: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters_region_id: Optional[UUID] = None
    description: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True


class DenominationCreate(DenominationBase):
    pass


class DenominationUpdate(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters_region_id: Optional[UUID] = None
    description: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None


class DenominationRead(DenominationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChurchBase(BaseModel):
    name: str
    denomination_id: UUID
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    kebele_id: Optional[UUID] = None
    community: Optional[str] = None
    address: Optional[str] = None
    year_established: Optional[int] = None
    membership_size: Optional[int] = None
    languages_used: list[str] = []
    service_schedules: list[dict] = []
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None


class ChurchCreate(ChurchBase):
    pass


class ChurchUpdate(BaseModel):
    name: Optional[str] = None
    denomination_id: Optional[UUID] = None
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    kebele_id: Optional[UUID] = None
    community: Optional[str] = None
    address: Optional[str] = None
    year_established: Optional[int] = None
    membership_size: Optional[int] = None
    languages_used: Optional[list[str]] = None
    service_schedules: Optional[list[dict]] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    is_verified: Optional[bool] = None
    verification_status: Optional[str] = None


class ChurchRead(ChurchBase):
    id: UUID
    is_verified: bool
    verification_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MinistryBase(BaseModel):
    name: str
    church_id: Optional[UUID] = None
    denomination_id: Optional[UUID] = None
    ministry_type: str
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    kebele_id: Optional[UUID] = None
    is_active: bool = True


class MinistryCreate(MinistryBase):
    pass


class MinistryUpdate(BaseModel):
    name: Optional[str] = None
    church_id: Optional[UUID] = None
    denomination_id: Optional[UUID] = None
    ministry_type: Optional[str] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    region_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    woreda_id: Optional[UUID] = None
    kebele_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class MinistryRead(MinistryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LeaderBase(BaseModel):
    church_id: UUID
    full_name: str
    role: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    is_primary: bool = False
    is_active: bool = True


class LeaderCreate(LeaderBase):
    pass


class LeaderUpdate(BaseModel):
    church_id: Optional[UUID] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    is_primary: Optional[bool] = None
    is_active: Optional[bool] = None


class LeaderRead(LeaderBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiasporaCommunityBase(BaseModel):
    name: str
    country: str
    city: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    membership_count: int = 0
    denomination_id: Optional[UUID] = None
    is_active: bool = True


class DiasporaCommunityCreate(DiasporaCommunityBase):
    pass


class DiasporaCommunityUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    membership_count: Optional[int] = None
    denomination_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class DiasporaCommunityRead(DiasporaCommunityBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DiasporaPartnershipBase(BaseModel):
    diaspora_community_id: UUID
    church_id: UUID
    partnership_type: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    status: str = "active"


class DiasporaPartnershipCreate(DiasporaPartnershipBase):
    pass


class DiasporaPartnershipRead(DiasporaPartnershipBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VerifyChurchResponse(BaseModel):
    id: UUID
    verification_status: Literal["verified"]
    is_verified: bool
