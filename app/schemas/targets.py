from uuid import UUID

from pydantic import Field

from app.domain.enums import TargetType
from app.schemas.common import ApiModel, JsonObject


class TargetCreate(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    type: TargetType
    base_url: str | None = Field(default=None, max_length=2000)
    model: str | None = Field(default=None, max_length=255)
    config: JsonObject = Field(default_factory=dict)


class TargetRead(TargetCreate):
    id: UUID
    is_enabled: bool


class ScopeValidationResponse(ApiModel):
    target_id: UUID
    allowed: bool
    reasons: list[str] = Field(default_factory=list)


class TargetHealthResponse(ApiModel):
    target_id: UUID
    reachable: bool
    details: JsonObject = Field(default_factory=dict)
