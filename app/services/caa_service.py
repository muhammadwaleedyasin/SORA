"""Country-specific CAA rule override resolution."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.caa import CaaRuleOverride, Country


async def get_country_overrides(
    db: AsyncSession,
    country_code: str,
) -> list[CaaRuleOverride]:
    """Fetch all active rule overrides for a country."""
    today = date.today()
    query = (
        select(CaaRuleOverride)
        .join(Country, Country.id == CaaRuleOverride.country_id)
        .where(
            Country.code == country_code.upper(),
            # Active rules: effective_from <= today (or null) AND effective_to >= today (or null)
            (CaaRuleOverride.effective_from <= today) | (CaaRuleOverride.effective_from.is_(None)),
            (CaaRuleOverride.effective_to >= today) | (CaaRuleOverride.effective_to.is_(None)),
        )
    )
    result = await db.execute(query)
    return list(result.scalars().all())


async def apply_country_overrides(
    db: AsyncSession,
    country_code: str,
    sail_level: str,
    final_grc: int,
    residual_arc: str,
) -> tuple[str, int, str, list[str]]:
    """Apply country-specific rule overrides.

    Returns (adjusted_sail, adjusted_grc, adjusted_arc, descriptions_of_changes).
    """
    overrides = await get_country_overrides(db, country_code)
    descriptions: list[str] = []

    adjusted_sail = sail_level
    adjusted_grc = final_grc
    adjusted_arc = residual_arc

    sail_order = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}

    for override in overrides:
        rule = override.rule_value

        if override.rule_type == "min_sail":
            min_sail = rule.get("min_sail", "I")
            if sail_order.get(adjusted_sail, 0) < sail_order.get(min_sail, 0):
                descriptions.append(
                    f"[{country_code}] {override.description or ''}: "
                    f"SAIL raised from {adjusted_sail} to {min_sail}"
                )
                adjusted_sail = min_sail

        elif override.rule_type == "additional_requirement":
            descriptions.append(
                f"[{country_code}] Additional requirement: {override.description or override.rule_key}"
            )

        elif override.rule_type == "grc_adjustment":
            adj = rule.get("adjustment", 0)
            adjusted_grc = max(1, adjusted_grc + adj)
            descriptions.append(
                f"[{country_code}] {override.description or ''}: GRC adjusted by {adj:+d}"
            )

    return adjusted_sail, adjusted_grc, adjusted_arc, descriptions
