from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.caa import CaaRuleOverride, Country
from app.schemas.caa import CaaRuleCreate, CaaRuleResponse, CountryResponse

router = APIRouter()


@router.get("/countries", response_model=list[CountryResponse])
async def list_countries(db: AsyncSession = Depends(get_db)):
    """List all supported countries."""
    result = await db.execute(select(Country).order_by(Country.name))
    return result.scalars().all()


@router.get("/countries/{code}/rules", response_model=list[CaaRuleResponse])
async def get_country_rules(code: str, db: AsyncSession = Depends(get_db)):
    """Get all rule overrides for a specific country."""
    country_result = await db.execute(
        select(Country).where(Country.code == code.upper())
    )
    country = country_result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country '{code}' not found")

    result = await db.execute(
        select(CaaRuleOverride).where(CaaRuleOverride.country_id == country.id)
    )
    return result.scalars().all()


@router.post("/countries/{code}/rules", response_model=CaaRuleResponse, status_code=201)
async def create_country_rule(
    code: str,
    rule: CaaRuleCreate,
    db: AsyncSession = Depends(get_db),
):
    """Add a CAA rule override for a country."""
    country_result = await db.execute(
        select(Country).where(Country.code == code.upper())
    )
    country = country_result.scalar_one_or_none()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country '{code}' not found")

    db_rule = CaaRuleOverride(country_id=country.id, **rule.model_dump())
    db.add(db_rule)
    await db.commit()
    await db.refresh(db_rule)
    return db_rule
