import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    NATIONAL_ADMIN = "NATIONAL_ADMIN"
    REGIONAL_ADMIN = "REGIONAL_ADMIN"
    FIELD_OFFICER = "FIELD_OFFICER"
    CHURCH_LEADER = "CHURCH_LEADER"
    DIASPORA_REP = "DIASPORA_REP"
    VIEWER = "VIEWER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    zones = relationship("Zone", back_populates="region", cascade="all, delete-orphan")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    region = relationship("Region", back_populates="zones")
    woredas = relationship("Woreda", back_populates="zone", cascade="all, delete-orphan")


class Woreda(Base):
    __tablename__ = "woredas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    zone = relationship("Zone", back_populates="woredas")
    kebeles = relationship("Kebele", back_populates="woreda", cascade="all, delete-orphan")
    churches = relationship("Church", back_populates="woreda")


class Kebele(Base):
    __tablename__ = "kebeles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    woreda_id = Column(Integer, ForeignKey("woredas.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    woreda = relationship("Woreda", back_populates="kebeles")


class Denomination(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    founded_year = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    churches = relationship("Church", back_populates="denomination")


class Church(Base):
    __tablename__ = "churches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    denomination_id = Column(Integer, ForeignKey("denominations.id"), nullable=False)
    woreda_id = Column(Integer, ForeignKey("woredas.id"), nullable=False)
    address = Column(Text)
    phone = Column(String(50))
    email = Column(String(255))
    established_year = Column(Integer)
    member_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    denomination = relationship("Denomination", back_populates="churches")
    woreda = relationship("Woreda", back_populates="churches")
    ministries = relationship("Ministry", back_populates="church", cascade="all, delete-orphan")
    leaders = relationship("ChurchLeader", back_populates="church", cascade="all, delete-orphan")
    diaspora_partnerships = relationship("DiasporaPartnership", back_populates="church")


class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    church_id = Column(Integer, ForeignKey("churches.id"), nullable=False)
    leader_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    church = relationship("Church", back_populates="ministries")


class ChurchLeader(Base):
    __tablename__ = "church_leaders"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    title = Column(String(100))
    church_id = Column(Integer, ForeignKey("churches.id"), nullable=False)
    phone = Column(String(50))
    email = Column(String(255))
    ordained_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    church = relationship("Church", back_populates="leaders")


class DiasporaCommunity(Base):
    __tablename__ = "diaspora_communities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100))
    contact_person = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    member_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    partnerships = relationship("DiasporaPartnership", back_populates="community", cascade="all, delete-orphan")


class DiasporaPartnership(Base):
    __tablename__ = "diaspora_partnerships"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("diaspora_communities.id"), nullable=False)
    church_id = Column(Integer, ForeignKey("churches.id"), nullable=False)
    partnership_type = Column(String(100))
    description = Column(Text)
    start_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    community = relationship("DiasporaCommunity", back_populates="partnerships")
    church = relationship("Church", back_populates="diaspora_partnerships")
