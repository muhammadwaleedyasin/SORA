"""Ground Risk Class calculator — iGRC lookup and mitigation application."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sora import (
    GrcMitigation,
    GrcMitigationLevel,
    IgrcDimensionClass,
    IgrcPopulationBand,
    IgrcValue,
)
from app.schemas.sora import GroundMitigationInput, MitigationDetail


async def calculate_igrc(
    db: AsyncSession,
    characteristic_dimension_m: float,
    max_speed_ms: float,
    max_population_density: float,
    is_controlled_ground: bool,
    is_over_assembly: bool,
) -> tuple[int | None, list[str]]:
    """Look up the intrinsic GRC from the database tables.

    Returns (igrc_value, warnings). igrc_value is None if out of scope.
    """
    warnings: list[str] = []

    # Find the matching dimension class (leftmost column where drone fits)
    dim_query = (
        select(IgrcDimensionClass)
        .where(
            IgrcDimensionClass.max_dimension_m >= characteristic_dimension_m,
            IgrcDimensionClass.max_speed_ms >= max_speed_ms,
        )
        .order_by(IgrcDimensionClass.sort_order.asc())
        .limit(1)
    )
    dim_result = await db.execute(dim_query)
    dim_class = dim_result.scalar_one_or_none()

    if dim_class is None:
        # Drone exceeds all dimension classes — outside SORA scope
        warnings.append(
            f"Drone dimensions ({characteristic_dimension_m}m, {max_speed_ms}m/s) "
            "exceed all iGRC table dimension classes. Operation may be outside SORA scope."
        )
        return None, warnings

    # Find the matching population band
    if is_over_assembly:
        band_query = (
            select(IgrcPopulationBand)
            .where(IgrcPopulationBand.is_assembly.is_(True))
            .limit(1)
        )
    elif is_controlled_ground:
        band_query = (
            select(IgrcPopulationBand)
            .where(IgrcPopulationBand.is_controlled.is_(True))
            .limit(1)
        )
    else:
        band_query = (
            select(IgrcPopulationBand)
            .where(
                IgrcPopulationBand.is_controlled.is_(False),
                IgrcPopulationBand.is_assembly.is_(False),
                IgrcPopulationBand.max_pop_density >= max_population_density,
            )
            .order_by(IgrcPopulationBand.sort_order.asc())
            .limit(1)
        )

    band_result = await db.execute(band_query)
    pop_band = band_result.scalar_one_or_none()

    if pop_band is None:
        warnings.append(
            f"Population density ({max_population_density} ppl/km²) exceeds all defined bands."
        )
        return None, warnings

    # Look up the iGRC value at the intersection
    val_query = select(IgrcValue).where(
        IgrcValue.dimension_class_id == dim_class.id,
        IgrcValue.population_band_id == pop_band.id,
    )
    val_result = await db.execute(val_query)
    igrc_entry = val_result.scalar_one_or_none()

    if igrc_entry is None or igrc_entry.is_out_of_scope:
        warnings.append("This combination is outside SORA scope (grey cell in iGRC table).")
        return None, warnings

    return igrc_entry.igrc_value, warnings


async def apply_ground_mitigations(
    db: AsyncSession,
    igrc: int,
    mitigations: list[GroundMitigationInput],
) -> tuple[int, list[MitigationDetail]]:
    """Apply ground risk mitigations to reduce iGRC to final GRC.

    Returns (final_grc, applied_mitigations).
    """
    applied: list[MitigationDetail] = []
    total_reduction = 0

    for mit_input in mitigations:
        query = (
            select(GrcMitigation, GrcMitigationLevel)
            .join(GrcMitigationLevel, GrcMitigation.id == GrcMitigationLevel.mitigation_id)
            .where(
                GrcMitigation.code == mit_input.code.upper(),
                GrcMitigationLevel.robustness == mit_input.robustness.lower(),
            )
        )
        result = await db.execute(query)
        row = result.first()
        if row is None:
            continue

        mitigation, level = row
        total_reduction += level.grc_reduction
        applied.append(
            MitigationDetail(
                code=mitigation.code,
                name=mitigation.name,
                robustness=level.robustness,
                reduction=level.grc_reduction,
            )
        )

    final_grc = max(1, igrc - total_reduction)
    return final_grc, applied
