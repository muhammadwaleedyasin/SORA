"""Idempotent seed runner — populates the database with SORA reference data.

Run with: python -m app.seed.seed_runner
"""

import asyncio

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session, engine
from app.models.base import Base
from app.models.caa import CaaRuleOverride, Country
from app.models.dma import DmaDimension, DmaQuestion
from app.models.sora import (
    ArcInitialRule,
    ArcMitigationEffect,
    ArcStrategicMitigation,
    GrcMitigation,
    GrcMitigationLevel,
    IgrcDimensionClass,
    IgrcPopulationBand,
    IgrcValue,
    OsoCatalogue,
    OsoSailRequirement,
    SailMatrix,
)
from app.seed.caa_norway import NORWAY_COUNTRY, NORWAY_RULES
from app.seed.dma_questions import DMA_DIMENSIONS, DMA_QUESTIONS
from app.seed.oso_data import OSO_CATALOGUE, OSO_REQUIREMENTS_BY_SAIL
from app.seed.sora_data import (
    ARC_INITIAL_RULES,
    ARC_MITIGATION_EFFECTS,
    ARC_STRATEGIC_MITIGATIONS,
    GRC_MITIGATION_LEVELS,
    GRC_MITIGATIONS,
    IGRC_DIMENSION_CLASSES,
    IGRC_POPULATION_BANDS,
    IGRC_VALUES,
    SAIL_MATRIX,
)


async def _upsert_rows(db: AsyncSession, model_class, data: list[dict]):
    """Insert rows if they don't already exist (by primary key or unique constraint)."""
    for row_data in data:
        pk = row_data.get("id")
        if pk is not None:
            existing = await db.get(model_class, pk)
            if existing:
                for k, v in row_data.items():
                    setattr(existing, k, v)
                continue
        obj = model_class(**row_data)
        db.add(obj)
    await db.flush()


async def seed_all(db: AsyncSession):
    """Seed all reference data."""
    print("Seeding iGRC dimension classes...")
    await _upsert_rows(db, IgrcDimensionClass, IGRC_DIMENSION_CLASSES)

    print("Seeding iGRC population bands...")
    await _upsert_rows(db, IgrcPopulationBand, IGRC_POPULATION_BANDS)

    print("Seeding iGRC values...")
    await _upsert_rows(db, IgrcValue, IGRC_VALUES)

    print("Seeding GRC mitigations...")
    await _upsert_rows(db, GrcMitigation, GRC_MITIGATIONS)
    await _upsert_rows(db, GrcMitigationLevel, GRC_MITIGATION_LEVELS)

    print("Seeding ARC rules...")
    await _upsert_rows(db, ArcInitialRule, ARC_INITIAL_RULES)
    await _upsert_rows(db, ArcStrategicMitigation, ARC_STRATEGIC_MITIGATIONS)
    await _upsert_rows(db, ArcMitigationEffect, ARC_MITIGATION_EFFECTS)

    print("Seeding SAIL matrix...")
    await _upsert_rows(db, SailMatrix, SAIL_MATRIX)

    print("Seeding OSO catalogue...")
    oso_rows = [{"id": i + 1, **oso} for i, oso in enumerate(OSO_CATALOGUE)]
    await _upsert_rows(db, OsoCatalogue, oso_rows)

    print("Seeding OSO-SAIL requirements...")
    req_id = 1
    for oso_num, sail_reqs in OSO_REQUIREMENTS_BY_SAIL.items():
        oso_id = oso_num  # oso_number matches id in catalogue
        for sail_level, robustness in sail_reqs.items():
            await _upsert_rows(db, OsoSailRequirement, [{
                "id": req_id,
                "oso_id": oso_id,
                "sail_level": sail_level,
                "robustness": robustness,
            }])
            req_id += 1

    print("Seeding Norway CAA data...")
    await _upsert_rows(db, Country, [NORWAY_COUNTRY])
    rule_rows = [{"id": i + 1, **rule} for i, rule in enumerate(NORWAY_RULES)]
    await _upsert_rows(db, CaaRuleOverride, rule_rows)

    print("Seeding DMA dimensions...")
    await _upsert_rows(db, DmaDimension, DMA_DIMENSIONS)

    print("Seeding DMA questions...")
    q_rows = [{"id": i + 1, **q} for i, q in enumerate(DMA_QUESTIONS)]
    await _upsert_rows(db, DmaQuestion, q_rows)

    await db.commit()
    print("Seeding complete!")


async def main():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data
    async with async_session() as db:
        await seed_all(db)


if __name__ == "__main__":
    asyncio.run(main())
