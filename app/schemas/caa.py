from datetime import date

from pydantic import BaseModel, Field


class CountryResponse(BaseModel):
    id: int
    code: str
    name: str
    regulatory_body: str
    sora_version: str
    notes: str | None

    model_config = {"from_attributes": True}


class CaaRuleCreate(BaseModel):
    rule_type: str = Field(..., max_length=50)
    rule_key: str = Field(..., max_length=100)
    rule_value: dict
    description: str | None = None
    effective_from: date | None = None
    effective_to: date | None = None


class CaaRuleResponse(BaseModel):
    id: int
    country_id: int
    rule_type: str
    rule_key: str
    rule_value: dict
    description: str | None
    effective_from: date | None
    effective_to: date | None

    model_config = {"from_attributes": True}
