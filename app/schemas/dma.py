import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DmaDimensionResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str | None
    weight: float
    sort_order: int

    model_config = {"from_attributes": True}


class DmaQuestionResponse(BaseModel):
    id: int
    dimension_id: int
    question_code: str
    question_text: str
    answer_type: str
    answer_options: dict | None
    weight: float
    max_score: int
    sort_order: int

    model_config = {"from_attributes": True}


class DmaAssessmentInput(BaseModel):
    organization_name: str | None = None
    responses: dict[str, int | float] = Field(
        ..., description="Map of question_code to answer value"
    )


class DimensionScore(BaseModel):
    dimension_code: str
    dimension_name: str
    score: float
    max_score: float
    percentage: float
    level: str


class DmaAssessmentResult(BaseModel):
    id: uuid.UUID
    organization_name: str | None
    dimension_scores: list[DimensionScore]
    overall_score: float
    overall_percentage: float
    maturity_level: str
    recommendations: list[str]
    created_at: datetime
