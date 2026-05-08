import uuid
from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class FieldRegistration(Base):
    __tablename__ = "field_registrations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    church_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("churches.id", ondelete="CASCADE"), nullable=False)
    field_officer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    gps_lat: Mapped[float] = mapped_column(Float, nullable=False)
    gps_lng: Mapped[float] = mapped_column(Float, nullable=False)
    gps_accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    location: Mapped[str | None] = mapped_column(Geometry("POINT", srid=4326), nullable=True)
    device_metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    photos: Mapped[list] = mapped_column(JSONB, default=list)
    registration_status: Mapped[str] = mapped_column(String(50), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
