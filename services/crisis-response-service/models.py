import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from database import Base


class IncidentSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    RESOLVED = "RESOLVED"


class VolunteerStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    DEPLOYED = "DEPLOYED"
    UNAVAILABLE = "UNAVAILABLE"


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(SAEnum(IncidentSeverity), default=IncidentSeverity.MEDIUM)
    status = Column(SAEnum(IncidentStatus), default=IncidentStatus.REPORTED)
    location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    reported_by = Column(Integer, nullable=False)
    woreda_id = Column(Integer)
    affected_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    volunteers = relationship("VolunteerDeployment", back_populates="incident")
    distributions = relationship("ReliefDistribution", back_populates="incident")


class Volunteer(Base):
    __tablename__ = "volunteers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50))
    email = Column(String(255))
    skills = Column(Text)
    church_id = Column(Integer)
    status = Column(SAEnum(VolunteerStatus), default=VolunteerStatus.AVAILABLE)
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deployments = relationship("VolunteerDeployment", back_populates="volunteer")


class VolunteerDeployment(Base):
    __tablename__ = "volunteer_deployments"
    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    deployed_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime)
    notes = Column(Text)
    volunteer = relationship("Volunteer", back_populates="deployments")
    incident = relationship("Incident", back_populates="volunteers")


class ReliefDistribution(Base):
    __tablename__ = "relief_distributions"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50))
    distributed_to = Column(String(255))
    distributed_at = Column(DateTime, default=datetime.utcnow)
    distributed_by = Column(Integer)
    notes = Column(Text)
    incident = relationship("Incident", back_populates="distributions")
