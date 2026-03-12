import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Numeric, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class DroneModel(Base):
    __tablename__ = "drone_models"
    __table_args__ = (UniqueConstraint("manufacturer", "model_name"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    manufacturer: Mapped[str] = mapped_column(String(200), nullable=False)
    model_name: Mapped[str] = mapped_column(String(200), nullable=False)
    mtom_kg: Mapped[float] = mapped_column(Numeric(8, 3), nullable=False)
    characteristic_dimension_m: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    max_speed_ms: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    propulsion_type: Mapped[str] = mapped_column(String(50), nullable=False)
    has_parachute: Mapped[bool] = mapped_column(Boolean, default=False)
    has_fts: Mapped[bool] = mapped_column(Boolean, default=False)
    energy_type: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
