import uuid

from pydantic import BaseModel, Field, model_validator


class GroundMitigationInput(BaseModel):
    code: str = Field(..., description="Mitigation code, e.g. 'M1A'")
    robustness: str = Field(..., pattern=r"^(none|low|medium|high)$")


class AirMitigationInput(BaseModel):
    code: str = Field(..., description="Strategic mitigation code")
    robustness: str = Field(..., pattern=r"^(low|medium|high)$")


class SoraCalculationInput(BaseModel):
    """Input for a full SORA assessment."""
    # Drone — either reference an existing model or provide specs inline
    drone_model_id: uuid.UUID | None = None
    mtom_kg: float | None = Field(None, gt=0)
    characteristic_dimension_m: float | None = Field(None, gt=0)
    max_speed_ms: float | None = Field(None, gt=0)

    # Ground risk inputs
    max_population_density: float = Field(..., ge=0, description="People per km²")
    is_over_assembly: bool = False
    is_controlled_ground: bool = False
    ground_mitigations: list[GroundMitigationInput] = []

    # Air risk inputs
    flight_altitude_m: float = Field(..., gt=0, description="Flight altitude in meters AGL")
    airspace_class: str = Field(..., pattern=r"^[A-G]$")
    is_airport_environment: bool = False
    is_segregated_airspace: bool = False
    strategic_mitigations: list[AirMitigationInput] = []

    # Country context
    country_code: str = Field("NO", min_length=2, max_length=2)

    @model_validator(mode="after")
    def check_drone_specs(self):
        has_id = self.drone_model_id is not None
        has_specs = all([self.mtom_kg, self.characteristic_dimension_m, self.max_speed_ms])
        if not has_id and not has_specs:
            raise ValueError("Provide either drone_model_id or all of (mtom_kg, characteristic_dimension_m, max_speed_ms)")
        return self


class MitigationDetail(BaseModel):
    code: str
    name: str
    robustness: str
    reduction: int


class OsoRequirement(BaseModel):
    oso_number: int
    title: str
    category: str
    required_robustness: str  # O, L, M, H


class SoraCalculationResult(BaseModel):
    intrinsic_grc: int
    applied_ground_mitigations: list[MitigationDetail]
    final_grc: int
    initial_arc: str
    applied_strategic_mitigations: list[MitigationDetail]
    residual_arc: str
    sail_level: str
    oso_requirements: list[OsoRequirement]
    country_overrides_applied: list[str]
    warnings: list[str]


class GrcCalculationInput(BaseModel):
    """Input for GRC-only calculation."""
    mtom_kg: float | None = Field(None, gt=0)
    characteristic_dimension_m: float | None = Field(None, gt=0)
    max_speed_ms: float | None = Field(None, gt=0)
    drone_model_id: uuid.UUID | None = None
    max_population_density: float = Field(..., ge=0)
    is_over_assembly: bool = False
    is_controlled_ground: bool = False
    ground_mitigations: list[GroundMitigationInput] = []


class GrcResult(BaseModel):
    intrinsic_grc: int
    applied_mitigations: list[MitigationDetail]
    final_grc: int
    warnings: list[str]


class ArcCalculationInput(BaseModel):
    """Input for ARC-only calculation."""
    flight_altitude_m: float = Field(..., gt=0)
    airspace_class: str = Field(..., pattern=r"^[A-G]$")
    is_airport_environment: bool = False
    is_segregated_airspace: bool = False
    strategic_mitigations: list[AirMitigationInput] = []


class ArcResult(BaseModel):
    initial_arc: str
    applied_mitigations: list[MitigationDetail]
    residual_arc: str
    warnings: list[str]


class SailMatrixEntry(BaseModel):
    final_grc: int
    residual_arc: str
    sail_level: str

    model_config = {"from_attributes": True}


class OsoResponse(BaseModel):
    oso_number: int
    title: str
    category: str
    description: str | None
    requirements_by_sail: dict[str, str] | None = None

    model_config = {"from_attributes": True}
