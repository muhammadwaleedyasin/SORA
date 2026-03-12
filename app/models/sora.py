from sqlalchemy import Boolean, Integer, Numeric, String, Text, UniqueConstraint, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

ARC_CHECK = CheckConstraint("initial_arc IN ('ARC-a','ARC-b','ARC-c','ARC-d')")
SAIL_CHECK = CheckConstraint("sail_level IN ('I','II','III','IV','V','VI')")


class IgrcDimensionClass(Base):
    """Columns of the iGRC table — defined by max characteristic dimension AND max speed."""
    __tablename__ = "igrc_dimension_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_label: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    max_dimension_m: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    max_speed_ms: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)


class IgrcPopulationBand(Base):
    """Rows of the iGRC table — population density bands."""
    __tablename__ = "igrc_population_bands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    band_label: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    max_pop_density: Mapped[float | None] = mapped_column(Numeric(10, 2))
    is_controlled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_assembly: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)


class IgrcValue(Base):
    """Intersection values in the iGRC table."""
    __tablename__ = "igrc_values"
    __table_args__ = (UniqueConstraint("dimension_class_id", "population_band_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dimension_class_id: Mapped[int] = mapped_column(ForeignKey("igrc_dimension_classes.id"), nullable=False)
    population_band_id: Mapped[int] = mapped_column(ForeignKey("igrc_population_bands.id"), nullable=False)
    igrc_value: Mapped[int | None] = mapped_column(Integer)
    is_out_of_scope: Mapped[bool] = mapped_column(Boolean, default=False)


class GrcMitigation(Base):
    """Ground risk mitigations (M1A, M1B, M1C)."""
    __tablename__ = "grc_mitigations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    max_reduction: Mapped[int] = mapped_column(Integer, default=0)


class GrcMitigationLevel(Base):
    """Robustness levels and their GRC reduction values."""
    __tablename__ = "grc_mitigation_levels"
    __table_args__ = (UniqueConstraint("mitigation_id", "robustness"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mitigation_id: Mapped[int] = mapped_column(ForeignKey("grc_mitigations.id"), nullable=False)
    robustness: Mapped[str] = mapped_column(String(10), nullable=False)
    grc_reduction: Mapped[int] = mapped_column(Integer, nullable=False)


class ArcInitialRule(Base):
    """Rules for determining initial ARC from airspace and operational context."""
    __tablename__ = "arc_initial_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rule_label: Mapped[str] = mapped_column(String(200), nullable=False)
    airspace_class: Mapped[str | None] = mapped_column(String(1))
    altitude_category: Mapped[str] = mapped_column(String(50), nullable=False)
    is_airport_env: Mapped[bool] = mapped_column(Boolean, default=False)
    is_segregated: Mapped[bool] = mapped_column(Boolean, default=False)
    is_atypical: Mapped[bool] = mapped_column(Boolean, default=False)
    initial_arc: Mapped[str] = mapped_column(String(5), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=0)


class ArcStrategicMitigation(Base):
    """Strategic mitigations for reducing ARC."""
    __tablename__ = "arc_strategic_mitigations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ArcMitigationEffect(Base):
    """Effect of strategic mitigations on ARC levels."""
    __tablename__ = "arc_mitigation_effects"
    __table_args__ = (UniqueConstraint("mitigation_id", "from_arc", "robustness_required"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mitigation_id: Mapped[int] = mapped_column(ForeignKey("arc_strategic_mitigations.id"), nullable=False)
    from_arc: Mapped[str] = mapped_column(String(5), nullable=False)
    to_arc: Mapped[str] = mapped_column(String(5), nullable=False)
    robustness_required: Mapped[str] = mapped_column(String(10), nullable=False)


class SailMatrix(Base):
    """SAIL determination: final_grc × residual_arc → SAIL level."""
    __tablename__ = "sail_matrix"
    __table_args__ = (UniqueConstraint("final_grc", "residual_arc"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    final_grc: Mapped[int] = mapped_column(Integer, nullable=False)
    residual_arc: Mapped[str] = mapped_column(String(5), nullable=False)
    sail_level: Mapped[str] = mapped_column(String(3), nullable=False)


class OsoCatalogue(Base):
    """The 24 Operational Safety Objectives."""
    __tablename__ = "oso_catalogue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    oso_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), nullable=False)


class OsoSailRequirement(Base):
    """Required robustness level for each OSO at each SAIL level."""
    __tablename__ = "oso_sail_requirements"
    __table_args__ = (UniqueConstraint("oso_id", "sail_level"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    oso_id: Mapped[int] = mapped_column(ForeignKey("oso_catalogue.id"), nullable=False)
    sail_level: Mapped[str] = mapped_column(String(3), nullable=False)
    robustness: Mapped[str] = mapped_column(String(1), nullable=False)  # O, L, M, H
