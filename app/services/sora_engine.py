"""SORA calculation engine — orchestrates GRC, ARC, SAIL, and OSO determination."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.drone import DroneModel
from app.schemas.sora import SoraCalculationInput, SoraCalculationResult
from app.services import arc_calculator, caa_service, grc_calculator, oso_mapper, sail_calculator


async def _resolve_drone_specs(
    db: AsyncSession,
    input_data: SoraCalculationInput,
) -> tuple[float, float, float]:
    """Resolve drone specs from DB or inline input.

    Returns (mtom_kg, characteristic_dimension_m, max_speed_ms).
    """
    if input_data.drone_model_id:
        query = select(DroneModel).where(DroneModel.id == input_data.drone_model_id)
        result = await db.execute(query)
        drone = result.scalar_one_or_none()
        if drone is None:
            raise ValueError(f"Drone model {input_data.drone_model_id} not found")
        return float(drone.mtom_kg), float(drone.characteristic_dimension_m), float(drone.max_speed_ms)

    # Use inline specs (validated by Pydantic model_validator)
    return input_data.mtom_kg, input_data.characteristic_dimension_m, input_data.max_speed_ms


async def calculate_sora(
    db: AsyncSession,
    input_data: SoraCalculationInput,
) -> SoraCalculationResult:
    """Run a full SORA assessment."""
    warnings: list[str] = []

    # 1. Resolve drone specs
    mtom_kg, char_dim, max_speed = await _resolve_drone_specs(db, input_data)

    # 2. Calculate iGRC
    igrc, grc_warnings = await grc_calculator.calculate_igrc(
        db,
        characteristic_dimension_m=char_dim,
        max_speed_ms=max_speed,
        max_population_density=input_data.max_population_density,
        is_controlled_ground=input_data.is_controlled_ground,
        is_over_assembly=input_data.is_over_assembly,
    )
    warnings.extend(grc_warnings)

    if igrc is None:
        # Out of scope — return early with maximum values
        return SoraCalculationResult(
            intrinsic_grc=0,
            applied_ground_mitigations=[],
            final_grc=0,
            initial_arc="ARC-d",
            applied_strategic_mitigations=[],
            residual_arc="ARC-d",
            sail_level="N/A",
            oso_requirements=[],
            country_overrides_applied=[],
            warnings=warnings + ["Operation is outside SORA scope. Full risk assessment required."],
        )

    # 3. Apply ground mitigations
    final_grc, applied_grc_mits = await grc_calculator.apply_ground_mitigations(
        db, igrc, input_data.ground_mitigations
    )

    # 4. Determine initial ARC
    initial_arc, arc_warnings = await arc_calculator.determine_initial_arc(
        db,
        flight_altitude_m=input_data.flight_altitude_m,
        airspace_class=input_data.airspace_class,
        is_airport_environment=input_data.is_airport_environment,
        is_segregated_airspace=input_data.is_segregated_airspace,
    )
    warnings.extend(arc_warnings)

    # 5. Apply strategic mitigations
    residual_arc, applied_arc_mits = await arc_calculator.apply_strategic_mitigations(
        db, initial_arc, input_data.strategic_mitigations
    )

    # 6. Determine SAIL
    sail_level, sail_warnings = await sail_calculator.determine_sail(db, final_grc, residual_arc)
    warnings.extend(sail_warnings)

    # 7. Apply country-specific overrides
    sail_level, final_grc, residual_arc, override_descriptions = await caa_service.apply_country_overrides(
        db, input_data.country_code, sail_level, final_grc, residual_arc
    )

    # 8. Map OSO requirements
    oso_reqs = await oso_mapper.get_oso_requirements(db, sail_level)

    return SoraCalculationResult(
        intrinsic_grc=igrc,
        applied_ground_mitigations=applied_grc_mits,
        final_grc=final_grc,
        initial_arc=initial_arc,
        applied_strategic_mitigations=applied_arc_mits,
        residual_arc=residual_arc,
        sail_level=sail_level,
        oso_requirements=oso_reqs,
        country_overrides_applied=override_descriptions,
        warnings=warnings,
    )
