"""Tests for the SORA calculation engine."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.sora import SoraCalculationInput
from app.services.sora_engine import calculate_sora


@pytest.mark.asyncio
async def test_basic_sora_calculation(db: AsyncSession):
    """Test a basic SORA calculation: small drone, sparsely populated, class G, below 120m."""
    input_data = SoraCalculationInput(
        mtom_kg=2.0,
        characteristic_dimension_m=0.5,
        max_speed_ms=20.0,
        max_population_density=100.0,
        is_over_assembly=False,
        is_controlled_ground=False,
        flight_altitude_m=50.0,
        airspace_class="G",
        country_code="NO",
    )
    result = await calculate_sora(db, input_data)

    assert result.intrinsic_grc == 3  # <1m & <=25m/s, sparsely populated
    assert result.final_grc == 3  # No mitigations applied
    assert result.initial_arc == "ARC-b"  # Class G, below 120m
    assert result.residual_arc == "ARC-b"
    assert result.sail_level == "II"  # GRC=3, ARC-b → SAIL II
    assert len(result.oso_requirements) == 24
    assert result.warnings == []


@pytest.mark.asyncio
async def test_controlled_ground_low_grc(db: AsyncSession):
    """Test controlled ground area gives lower GRC."""
    input_data = SoraCalculationInput(
        mtom_kg=2.0,
        characteristic_dimension_m=0.5,
        max_speed_ms=20.0,
        max_population_density=0.0,
        is_controlled_ground=True,
        flight_altitude_m=50.0,
        airspace_class="G",
        country_code="NO",
    )
    result = await calculate_sora(db, input_data)

    assert result.intrinsic_grc == 1  # Controlled ground, small drone


@pytest.mark.asyncio
async def test_mitigations_reduce_grc(db: AsyncSession):
    """Test that ground mitigations reduce GRC."""
    from app.schemas.sora import GroundMitigationInput

    input_data = SoraCalculationInput(
        mtom_kg=2.0,
        characteristic_dimension_m=0.5,
        max_speed_ms=20.0,
        max_population_density=100.0,
        is_controlled_ground=False,
        ground_mitigations=[
            GroundMitigationInput(code="M1B", robustness="low"),
        ],
        flight_altitude_m=50.0,
        airspace_class="G",
        country_code="NO",
    )
    result = await calculate_sora(db, input_data)

    assert result.intrinsic_grc == 3
    assert result.final_grc == 2  # M1B low gives -1 reduction
    assert len(result.applied_ground_mitigations) == 1


@pytest.mark.asyncio
async def test_airport_environment_gives_arc_d(db: AsyncSession):
    """Test that airport environment results in ARC-d."""
    input_data = SoraCalculationInput(
        mtom_kg=2.0,
        characteristic_dimension_m=0.5,
        max_speed_ms=20.0,
        max_population_density=100.0,
        flight_altitude_m=50.0,
        airspace_class="G",
        is_airport_environment=True,
        country_code="NO",
    )
    result = await calculate_sora(db, input_data)

    assert result.initial_arc == "ARC-d"


@pytest.mark.asyncio
async def test_high_population_high_sail(db: AsyncSession):
    """Test that high population density + controlled airspace leads to high SAIL."""
    input_data = SoraCalculationInput(
        mtom_kg=10.0,
        characteristic_dimension_m=2.0,
        max_speed_ms=30.0,
        max_population_density=5000.0,
        flight_altitude_m=50.0,
        airspace_class="C",
        country_code="NO",
    )
    result = await calculate_sora(db, input_data)

    assert result.intrinsic_grc >= 5  # Higher GRC for populated area, larger drone
    assert result.initial_arc in ("ARC-c", "ARC-d")
    # SAIL should be IV or higher
    sail_order = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
    assert sail_order[result.sail_level] >= 4
