"""OSO requirement mapper — returns required robustness levels for a given SAIL."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sora import OsoCatalogue, OsoSailRequirement
from app.schemas.sora import OsoRequirement


async def get_oso_requirements(
    db: AsyncSession,
    sail_level: str,
) -> list[OsoRequirement]:
    """Get all 24 OSOs with their required robustness for the given SAIL level."""
    query = (
        select(OsoCatalogue, OsoSailRequirement)
        .join(OsoSailRequirement, OsoCatalogue.id == OsoSailRequirement.oso_id)
        .where(OsoSailRequirement.sail_level == sail_level)
        .order_by(OsoCatalogue.oso_number)
    )
    result = await db.execute(query)
    rows = result.all()

    return [
        OsoRequirement(
            oso_number=oso.oso_number,
            title=oso.title,
            category=oso.category,
            required_robustness=req.robustness,
        )
        for oso, req in rows
    ]
