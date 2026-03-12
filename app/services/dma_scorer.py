"""DMA (Drone Maturity Assessment) scoring engine."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dma import DmaAssessment, DmaDimension, DmaQuestion
from app.schemas.dma import DimensionScore, DmaAssessmentInput, DmaAssessmentResult

MATURITY_LEVELS = [
    (1.0, 1.5, "Initial"),
    (1.5, 2.5, "Managed"),
    (2.5, 3.5, "Defined"),
    (3.5, 4.5, "Measured"),
    (4.5, 5.01, "Optimized"),
]


def _maturity_level(score: float) -> str:
    for low, high, level in MATURITY_LEVELS:
        if low <= score < high:
            return level
    return "Initial" if score < 1.0 else "Optimized"


def _dimension_level(percentage: float) -> str:
    if percentage >= 90:
        return "Optimized"
    elif percentage >= 70:
        return "Measured"
    elif percentage >= 50:
        return "Defined"
    elif percentage >= 30:
        return "Managed"
    else:
        return "Initial"


async def run_assessment(
    db: AsyncSession,
    input_data: DmaAssessmentInput,
) -> DmaAssessmentResult:
    """Score a DMA assessment from questionnaire responses."""

    # Load all dimensions and questions
    dim_result = await db.execute(
        select(DmaDimension).order_by(DmaDimension.sort_order)
    )
    dimensions = dim_result.scalars().all()

    q_result = await db.execute(
        select(DmaQuestion).order_by(DmaQuestion.sort_order)
    )
    questions = q_result.scalars().all()

    # Group questions by dimension
    dim_questions: dict[int, list[DmaQuestion]] = {}
    for q in questions:
        dim_questions.setdefault(q.dimension_id, []).append(q)

    # Calculate per-dimension scores
    dimension_scores: list[DimensionScore] = []
    dim_score_map: dict[str, float] = {}
    recommendations: list[str] = []

    for dim in dimensions:
        qs = dim_questions.get(dim.id, [])
        if not qs:
            continue

        weighted_sum = 0.0
        weight_total = 0.0

        for q in qs:
            answer = input_data.responses.get(q.question_code)
            if answer is None:
                continue
            # Normalize answer to 0-1 scale, then multiply by weight
            normalized = float(answer) / q.max_score
            weighted_sum += normalized * float(q.weight)
            weight_total += float(q.weight)

        if weight_total == 0:
            continue

        # Score on 1-5 scale
        raw_score = (weighted_sum / weight_total) * 5.0
        score = round(raw_score, 2)
        max_score = 5.0
        percentage = round((score / max_score) * 100, 1)
        level = _dimension_level(percentage)

        dimension_scores.append(
            DimensionScore(
                dimension_code=dim.code,
                dimension_name=dim.name,
                score=score,
                max_score=max_score,
                percentage=percentage,
                level=level,
            )
        )
        dim_score_map[dim.code] = score

        # Generate recommendations for weak areas
        if percentage < 50:
            recommendations.append(
                f"{dim.name} ({dim.code}): Score {percentage}% - "
                f"significant improvement needed. Review processes and capabilities."
            )
        elif percentage < 70:
            recommendations.append(
                f"{dim.name} ({dim.code}): Score {percentage}% - "
                f"moderate maturity. Consider formalizing procedures and training."
            )

    # Overall weighted score
    if not dimension_scores:
        overall_score = 0.0
    else:
        total_weight = sum(float(d.weight) for d in dimensions if d.code in dim_score_map)
        if total_weight > 0:
            overall_score = sum(
                dim_score_map[d.code] * float(d.weight)
                for d in dimensions
                if d.code in dim_score_map
            ) / total_weight
        else:
            overall_score = sum(ds.score for ds in dimension_scores) / len(dimension_scores)

    overall_score = round(overall_score, 2)
    overall_percentage = round((overall_score / 5.0) * 100, 1)
    maturity_level = _maturity_level(overall_score)

    # Persist assessment
    assessment = DmaAssessment(
        organization_name=input_data.organization_name,
        responses=input_data.responses,
        dimension_scores={ds.dimension_code: ds.score for ds in dimension_scores},
        overall_score=overall_score,
        maturity_level=maturity_level,
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)

    return DmaAssessmentResult(
        id=assessment.id,
        organization_name=assessment.organization_name,
        dimension_scores=dimension_scores,
        overall_score=overall_score,
        overall_percentage=overall_percentage,
        maturity_level=maturity_level,
        recommendations=recommendations,
        created_at=assessment.created_at,
    )
