"""SAIL determination from the GRC × ARC matrix."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sora import SailMatrix


async def determine_sail(
    db: AsyncSession,
    final_grc: int,
    residual_arc: str,
) -> tuple[str, list[str]]:
    """Look up the SAIL level from the matrix.

    GRC values are clamped: <=1 maps to row 1, >=7 maps to row 7 (or a dedicated >7 row).
    Returns (sail_level, warnings).
    """
    warnings: list[str] = []

    # Clamp GRC for lookup
    lookup_grc = max(1, min(final_grc, 7))

    query = select(SailMatrix).where(
        SailMatrix.final_grc == lookup_grc,
        SailMatrix.residual_arc == residual_arc,
    )
    result = await db.execute(query)
    entry = result.scalar_one_or_none()

    if entry is None:
        warnings.append(f"No SAIL matrix entry found for GRC={lookup_grc}, ARC={residual_arc}.")
        return "VI", warnings  # Default to most conservative

    return entry.sail_level, warnings
