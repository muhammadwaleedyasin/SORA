import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DroneModelCreate(BaseModel):
    manufacturer: str = Field(..., max_length=200)
    model_name: str = Field(..., max_length=200)
    mtom_kg: float = Field(..., gt=0, description="Max takeoff mass in kg")
    characteristic_dimension_m: float = Field(..., gt=0, description="Largest dimension in meters")
    max_speed_ms: float = Field(..., gt=0, description="Max speed in m/s")
    propulsion_type: str = Field(..., pattern=r"^(multirotor|fixed_wing|hybrid|vtol)$")
    has_parachute: bool = False
    has_fts: bool = False
    energy_type: str | None = None
    notes: str | None = None


class DroneModelUpdate(BaseModel):
    manufacturer: str | None = None
    model_name: str | None = None
    mtom_kg: float | None = Field(None, gt=0)
    characteristic_dimension_m: float | None = Field(None, gt=0)
    max_speed_ms: float | None = Field(None, gt=0)
    propulsion_type: str | None = Field(None, pattern=r"^(multirotor|fixed_wing|hybrid|vtol)$")
    has_parachute: bool | None = None
    has_fts: bool | None = None
    energy_type: str | None = None
    notes: str | None = None


class DroneModelResponse(BaseModel):
    id: uuid.UUID
    manufacturer: str
    model_name: str
    mtom_kg: float
    characteristic_dimension_m: float
    max_speed_ms: float
    propulsion_type: str
    has_parachute: bool
    has_fts: bool
    energy_type: str | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
