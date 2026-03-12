"""Air Risk Class calculator — initial ARC determination and strategic mitigation."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sora import ArcInitialRule, ArcMitigationEffect, ArcStrategicMitigation
from app.schemas.sora import AirMitigationInput, MitigationDetail

ARC_ORDER = ["ARC-a", "ARC-b", "ARC-c", "ARC-d"]


def _altitude_category(altitude_m: float) -> str:
    if altitude_m <= 120:
        return "below_120m"
    elif altitude_m <= 18288:  # FL600 ≈ 18,288m
        return "120m_to_FL600"
    else:
        return "above_FL600"


async def determine_initial_arc(
    db: AsyncSession,
    flight_altitude_m: float,
    airspace_class: str,
    is_airport_environment: bool,
    is_segregated_airspace: bool,
) -> tuple[str, list[str]]:
    """Determine the initial ARC based on operational context.

    Returns (initial_arc, warnings).
    """
    warnings: list[str] = []
    alt_cat = _altitude_category(flight_altitude_m)

    # Query rules matching the operational context, ordered by priority (highest first)
    query = (
        select(ArcInitialRule)
        .where(ArcInitialRule.altitude_category == alt_cat)
        .order_by(ArcInitialRule.priority.desc())
    )
    result = await db.execute(query)
    rules = result.scalars().all()

    for rule in rules:
        # Check airspace class match (None = any airspace)
        if rule.airspace_class is not None and rule.airspace_class != airspace_class.upper():
            continue
        # Check airport environment
        if rule.is_airport_env and not is_airport_environment:
            continue
        # Check segregated airspace
        if rule.is_segregated and not is_segregated_airspace:
            continue
        # First matching rule wins
        return rule.initial_arc, warnings

    # Fallback: if no rule matched, default to ARC-b for below 120m in uncontrolled
    if alt_cat == "below_120m" and airspace_class.upper() in ("F", "G"):
        warnings.append("No explicit ARC rule matched; defaulting to ARC-b for low-altitude uncontrolled airspace.")
        return "ARC-b", warnings

    warnings.append("No ARC rule matched the given parameters; defaulting to ARC-d (most conservative).")
    return "ARC-d", warnings


async def apply_strategic_mitigations(
    db: AsyncSession,
    initial_arc: str,
    mitigations: list[AirMitigationInput],
) -> tuple[str, list[MitigationDetail]]:
    """Apply strategic mitigations to reduce ARC.

    Returns (residual_arc, applied_mitigations).
    """
    applied: list[MitigationDetail] = []
    current_arc = initial_arc

    for mit_input in mitigations:
        query = (
            select(ArcStrategicMitigation, ArcMitigationEffect)
            .join(ArcMitigationEffect, ArcStrategicMitigation.id == ArcMitigationEffect.mitigation_id)
            .where(
                ArcStrategicMitigation.code == mit_input.code.upper(),
                ArcMitigationEffect.from_arc == current_arc,
                ArcMitigationEffect.robustness_required <= mit_input.robustness.lower(),
            )
        )
        result = await db.execute(query)
        row = result.first()
        if row is None:
            continue

        mitigation, effect = row
        arc_before_idx = ARC_ORDER.index(current_arc)
        arc_after_idx = ARC_ORDER.index(effect.to_arc)
        reduction = arc_before_idx - arc_after_idx

        applied.append(
            MitigationDetail(
                code=mitigation.code,
                name=mitigation.name,
                robustness=mit_input.robustness,
                reduction=reduction,
            )
        )
        current_arc = effect.to_arc

    return current_arc, applied
