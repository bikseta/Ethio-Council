import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Date, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum

from database import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    NATIONAL_ADMIN = "NATIONAL_ADMIN"
    REGIONAL_ADMIN = "REGIONAL_ADMIN"
    ZONAL_ADMIN = "ZONAL_ADMIN"
    LOCAL_ADMIN = "LOCAL_ADMIN"
    DENOMINATION_ADMIN = "DENOMINATION_ADMIN"
    VIEWER = "VIEWER"

class MemberStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING = "PENDING"

class CrisisSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CrisisStatus(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESPONDING = "RESPONDING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class Denomination(Base):
    __tablename__ = "denominations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, unique=True)
    name_am = Column(String(200))
    abbreviation = Column(String(20))
    founded_year = Column(Integer)
    headquarters_city = Column(String(100))
    website = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    churches = relationship("Church", back_populates="denomination")
    users = relationship("User", back_populates="denomination")

class Region(Base):
    __tablename__ = "regions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    name_am = Column(String(100))
    code = Column(String(10), unique=True)
    boundary = Column(Geometry("MULTIPOLYGON", srid=4326))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    zones = relationship("Zone", back_populates="region")
    users = relationship("User", back_populates="region")

class Zone(Base):
    __tablename__ = "zones"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    name_am = Column(String(100))
    code = Column(String(10))
    boundary = Column(Geometry("MULTIPOLYGON", srid=4326))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    region = relationship("Region", back_populates="zones")
    woredas = relationship("Woreda", back_populates="zone")

class Woreda(Base):
    __tablename__ = "woredas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    name_am = Column(String(100))
    code = Column(String(10))
    boundary = Column(Geometry("MULTIPOLYGON", srid=4326))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    zone = relationship("Zone", back_populates="woredas")
    churches = relationship("Church", back_populates="woreda")

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    full_name = Column(String(200), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.VIEWER)
    denomination_id = Column(UUID(as_uuid=True), ForeignKey("denominations.id", ondelete="SET NULL"), nullable=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    denomination = relationship("Denomination", back_populates="users")
    region = relationship("Region", back_populates="users")

class Church(Base):
    __tablename__ = "churches"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    denomination_id = Column(UUID(as_uuid=True), ForeignKey("denominations.id", ondelete="CASCADE"), nullable=False)
    woreda_id = Column(UUID(as_uuid=True), ForeignKey("woredas.id", ondelete="SET NULL"))
    name = Column(String(200), nullable=False)
    name_am = Column(String(200))
    pastor_name = Column(String(200))
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    location = Column(Geometry("POINT", srid=4326))
    member_count = Column(Integer, default=0)
    established_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    denomination = relationship("Denomination", back_populates="churches")
    woreda = relationship("Woreda", back_populates="churches")
    members = relationship("Member", back_populates="church")

class Member(Base):
    __tablename__ = "members"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    church_id = Column(UUID(as_uuid=True), ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    denomination_id = Column(UUID(as_uuid=True), ForeignKey("denominations.id", ondelete="SET NULL"))
    full_name = Column(String(200), nullable=False)
    full_name_am = Column(String(200))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    location = Column(Geometry("POINT", srid=4326))
    status = Column(SAEnum(MemberStatus, name="member_status"), default=MemberStatus.ACTIVE)
    baptism_date = Column(Date)
    membership_date = Column(Date)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    church = relationship("Church", back_populates="members")

class CrisisReport(Base):
    __tablename__ = "crisis_reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    church_id = Column(UUID(as_uuid=True), ForeignKey("churches.id", ondelete="SET NULL"))
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id", ondelete="SET NULL"))
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(SAEnum(CrisisSeverity, name="crisis_severity"), nullable=False, default=CrisisSeverity.MEDIUM)
    status = Column(SAEnum(CrisisStatus, name="crisis_status"), nullable=False, default=CrisisStatus.OPEN)
    location = Column(Geometry("POINT", srid=4326))
    affected_count = Column(Integer, default=0)
    response_notes = Column(Text)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
