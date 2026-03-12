import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.dma import DmaAssessment, DmaDimension, DmaQuestion
from app.schemas.dma import (
    DmaAssessmentInput,
    DmaAssessmentResult,
    DmaDimensionResponse,
    DmaQuestionResponse,
)
from app.services.dma_scorer import run_assessment

router = APIRouter()


@router.get("/dimensions", response_model=list[DmaDimensionResponse])
async def list_dimensions(db: AsyncSession = Depends(get_db)):
    """List all DMA assessment dimensions."""
    result = await db.execute(select(DmaDimension).order_by(DmaDimension.sort_order))
    return result.scalars().all()


@router.get("/questions", response_model=list[DmaQuestionResponse])
async def list_questions(
    dimension: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """List DMA questions, optionally filtered by dimension code."""
    query = select(DmaQuestion).order_by(DmaQuestion.sort_order)
    if dimension:
        query = query.join(DmaDimension).where(DmaDimension.code == dimension.upper())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/assess", response_model=DmaAssessmentResult)
async def assess(
    input_data: DmaAssessmentInput,
    db: AsyncSession = Depends(get_db),
):
    """Submit questionnaire responses and get maturity assessment results."""
    result = await run_assessment(db, input_data)
    return result


@router.get("/assessments/{assessment_id}", response_model=DmaAssessmentResult)
async def get_assessment(assessment_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Retrieve a saved DMA assessment."""
    result = await db.execute(
        select(DmaAssessment).where(DmaAssessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    from app.schemas.dma import DimensionScore
    from app.services.dma_scorer import _dimension_level

    # Load dimension names
    dim_result = await db.execute(select(DmaDimension).order_by(DmaDimension.sort_order))
    dimensions = {d.code: d.name for d in dim_result.scalars().all()}

    dim_scores = []
    for code, score in assessment.dimension_scores.items():
        score_val = float(score)
        percentage = round((score_val / 5.0) * 100, 1)
        dim_scores.append(
            DimensionScore(
                dimension_code=code,
                dimension_name=dimensions.get(code, code),
                score=score_val,
                max_score=5.0,
                percentage=percentage,
                level=_dimension_level(percentage),
            )
        )

    overall = float(assessment.overall_score)
    return DmaAssessmentResult(
        id=assessment.id,
        organization_name=assessment.organization_name,
        dimension_scores=dim_scores,
        overall_score=overall,
        overall_percentage=round((overall / 5.0) * 100, 1),
        maturity_level=assessment.maturity_level,
        recommendations=[],
        created_at=assessment.created_at,
    )
