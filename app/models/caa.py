from datetime import date

from sqlalchemy import JSON, Date, Integer, String, Text, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    regulatory_body: Mapped[str] = mapped_column(String(200), nullable=False)
    sora_version: Mapped[str] = mapped_column(String(10), default="2.5")
    notes: Mapped[str | None] = mapped_column(Text)


class CaaRuleOverride(Base):
    """Country-specific regulatory rule overrides."""
    __tablename__ = "caa_rule_overrides"
    __table_args__ = (UniqueConstraint("country_id", "rule_type", "rule_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    rule_key: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_value: Mapped[dict] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    effective_from: Mapped[date | None] = mapped_column(Date)
    effective_to: Mapped[date | None] = mapped_column(Date)
