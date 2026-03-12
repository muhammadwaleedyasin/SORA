import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, Numeric, String, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class DmaDimension(Base):
    __tablename__ = "dma_dimensions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    weight: Mapped[float] = mapped_column(Numeric(4, 3), default=1.0)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)


class DmaQuestion(Base):
    __tablename__ = "dma_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dimension_id: Mapped[int] = mapped_column(ForeignKey("dma_dimensions.id"), nullable=False)
    question_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    answer_type: Mapped[str] = mapped_column(String(20), default="scale")
    answer_options: Mapped[dict | None] = mapped_column(JSON)
    weight: Mapped[float] = mapped_column(Numeric(4, 3), default=1.0)
    max_score: Mapped[int] = mapped_column(Integer, default=5)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)


class DmaAssessment(Base):
    __tablename__ = "dma_assessments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    organization_name: Mapped[str | None] = mapped_column(String(300))
    responses: Mapped[dict] = mapped_column(JSON, nullable=False)
    dimension_scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    overall_score: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    maturity_level: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
