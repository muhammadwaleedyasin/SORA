from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.sora import OsoCatalogue, OsoSailRequirement, SailMatrix
from app.schemas.sora import (
    ArcCalculationInput,
    ArcResult,
    GrcCalculationInput,
    GrcResult,
    OsoResponse,
    SailMatrixEntry,
    SoraCalculationInput,
    SoraCalculationResult,
)
from app.services import arc_calculator, grc_calculator, sora_engine

router = APIRouter()


@router.post("/calculate", response_model=SoraCalculationResult)
async def calculate_sora(
    input_data: SoraCalculationInput,
    db: AsyncSession = Depends(get_db),
):
    """Run a full SORA assessment — calculates GRC, ARC, SAIL, and maps OSOs."""
    try:
        result = await sora_engine.calculate_sora(db, input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.post("/grc", response_model=GrcResult)
async def calculate_grc(
    input_data: GrcCalculationInput,
    db: AsyncSession = Depends(get_db),
):
    """Calculate Ground Risk Class only."""
    # Resolve drone specs
    char_dim = input_data.characteristic_dimension_m
    max_speed = input_data.max_speed_ms

    if input_data.drone_model_id:
        from app.models.drone import DroneModel
        result = await db.execute(
            select(DroneModel).where(DroneModel.id == input_data.drone_model_id)
        )
        drone = result.scalar_one_or_none()
        if not drone:
            raise HTTPException(status_code=404, detail="Drone model not found")
        char_dim = float(drone.characteristic_dimension_m)
        max_speed = float(drone.max_speed_ms)

    if not char_dim or not max_speed:
        raise HTTPException(
            status_code=400,
            detail="Provide drone_model_id or both characteristic_dimension_m and max_speed_ms",
        )

    igrc, warnings = await grc_calculator.calculate_igrc(
        db, char_dim, max_speed,
        input_data.max_population_density,
        input_data.is_controlled_ground,
        input_data.is_over_assembly,
    )

    if igrc is None:
        return GrcResult(intrinsic_grc=0, applied_mitigations=[], final_grc=0, warnings=warnings)

    final_grc, applied = await grc_calculator.apply_ground_mitigations(
        db, igrc, input_data.ground_mitigations
    )
    return GrcResult(intrinsic_grc=igrc, applied_mitigations=applied, final_grc=final_grc, warnings=warnings)


@router.post("/arc", response_model=ArcResult)
async def calculate_arc(
    input_data: ArcCalculationInput,
    db: AsyncSession = Depends(get_db),
):
    """Calculate Air Risk Class only."""
    initial_arc, warnings = await arc_calculator.determine_initial_arc(
        db,
        input_data.flight_altitude_m,
        input_data.airspace_class,
        input_data.is_airport_environment,
        input_data.is_segregated_airspace,
    )
    residual_arc, applied = await arc_calculator.apply_strategic_mitigations(
        db, initial_arc, input_data.strategic_mitigations
    )
    return ArcResult(
        initial_arc=initial_arc,
        applied_mitigations=applied,
        residual_arc=residual_arc,
        warnings=warnings,
    )


@router.get("/sail-matrix", response_model=list[SailMatrixEntry])
async def get_sail_matrix(db: AsyncSession = Depends(get_db)):
    """Return the full SAIL matrix for reference."""
    result = await db.execute(
        select(SailMatrix).order_by(SailMatrix.final_grc, SailMatrix.residual_arc)
    )
    return result.scalars().all()


@router.get("/osos", response_model=list[OsoResponse])
async def list_osos(db: AsyncSession = Depends(get_db)):
    """List all 24 Operational Safety Objectives."""
    result = await db.execute(select(OsoCatalogue).order_by(OsoCatalogue.oso_number))
    return result.scalars().all()


@router.get("/osos/{sail_level}", response_model=list[OsoResponse])
async def get_osos_for_sail(sail_level: str, db: AsyncSession = Depends(get_db)):
    """Get OSOs with required robustness for a specific SAIL level."""
    valid_levels = {"I", "II", "III", "IV", "V", "VI"}
    if sail_level.upper() not in valid_levels:
        raise HTTPException(status_code=400, detail=f"Invalid SAIL level. Must be one of: {valid_levels}")

    query = (
        select(OsoCatalogue, OsoSailRequirement)
        .join(OsoSailRequirement, OsoCatalogue.id == OsoSailRequirement.oso_id)
        .where(OsoSailRequirement.sail_level == sail_level.upper())
        .order_by(OsoCatalogue.oso_number)
    )
    result = await db.execute(query)
    rows = result.all()

    return [
        OsoResponse(
            oso_number=oso.oso_number,
            title=oso.title,
            category=oso.category,
            description=oso.description,
            requirements_by_sail={sail_level.upper(): req.robustness},
        )
        for oso, req in rows
    ]
