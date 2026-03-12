"""Tests for the DMA scoring engine."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.dma import DmaAssessmentInput
from app.services.dma_scorer import run_assessment


@pytest.mark.asyncio
async def test_perfect_scores(db: AsyncSession):
    """All 5s should give Optimized maturity."""
    responses = {f"OPS_0{i}": 5 for i in range(1, 6)}
    responses.update({f"TECH_0{i}": 5 for i in range(1, 6)})
    responses.update({f"SAFE_0{i}": 5 for i in range(1, 6)})
    responses.update({f"COMP_0{i}": 5 for i in range(1, 6)})
    responses.update({f"HR_0{i}": 5 for i in range(1, 6)})
    responses.update({f"DATA_0{i}": 5 for i in range(1, 6)})

    input_data = DmaAssessmentInput(
        organization_name="Test Municipality",
        responses=responses,
    )
    result = await run_assessment(db, input_data)

    assert result.maturity_level == "Optimized"
    assert result.overall_score == 5.0
    assert result.overall_percentage == 100.0
    assert len(result.recommendations) == 0


@pytest.mark.asyncio
async def test_low_scores(db: AsyncSession):
    """All 1s should give Initial maturity."""
    responses = {f"OPS_0{i}": 1 for i in range(1, 6)}
    responses.update({f"TECH_0{i}": 1 for i in range(1, 6)})
    responses.update({f"SAFE_0{i}": 1 for i in range(1, 6)})
    responses.update({f"COMP_0{i}": 1 for i in range(1, 6)})
    responses.update({f"HR_0{i}": 1 for i in range(1, 6)})
    responses.update({f"DATA_0{i}": 1 for i in range(1, 6)})

    input_data = DmaAssessmentInput(
        organization_name="Test Org",
        responses=responses,
    )
    result = await run_assessment(db, input_data)

    assert result.maturity_level == "Initial"
    assert result.overall_score == 1.0
    assert len(result.recommendations) > 0  # Should recommend improvements


@pytest.mark.asyncio
async def test_mixed_scores(db: AsyncSession):
    """Mixed scores should give intermediate maturity."""
    responses = {f"OPS_0{i}": 4 for i in range(1, 6)}
    responses.update({f"TECH_0{i}": 3 for i in range(1, 6)})
    responses.update({f"SAFE_0{i}": 2 for i in range(1, 6)})
    responses.update({f"COMP_0{i}": 3 for i in range(1, 6)})
    responses.update({f"HR_0{i}": 4 for i in range(1, 6)})
    responses.update({f"DATA_0{i}": 2 for i in range(1, 6)})

    input_data = DmaAssessmentInput(responses=responses)
    result = await run_assessment(db, input_data)

    assert 2.0 <= result.overall_score <= 4.0
    assert result.maturity_level in ("Managed", "Defined", "Measured")
    assert len(result.dimension_scores) == 6


@pytest.mark.asyncio
async def test_partial_responses(db: AsyncSession):
    """Should handle partial responses gracefully."""
    responses = {"OPS_01": 3, "OPS_02": 4, "SAFE_01": 5}

    input_data = DmaAssessmentInput(responses=responses)
    result = await run_assessment(db, input_data)

    # Should still produce scores for dimensions with answers
    assert len(result.dimension_scores) >= 2
    assert result.overall_score > 0
