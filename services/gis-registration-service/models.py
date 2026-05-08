import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import relationship
from database import Base


class RegistrationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class FieldRegistration(Base):
    __tablename__ = "field_registrations"
    id = Column(Integer, primary_key=True, index=True)
    church_id = Column(Integer, nullable=False)
    field_officer_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float)
    accuracy = Column(Float)
    address = Column(Text)
    notes = Column(Text)
    status = Column(SAEnum(RegistrationStatus), default=RegistrationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photos = relationship("RegistrationPhoto", back_populates="registration")


class RegistrationPhoto(Base):
    __tablename__ = "registration_photos"
    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("field_registrations.id"), nullable=False)
    s3_key = Column(String(500), nullable=False)
    caption = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    registration = relationship("FieldRegistration", back_populates="photos")
