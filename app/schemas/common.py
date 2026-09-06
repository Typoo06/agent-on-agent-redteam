from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

JsonObject = dict[str, Any]


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


def now_utc() -> datetime:
    return datetime.now(UTC)


class ResourceRef(ApiModel):
    id: UUID
    type: str = Field(min_length=1)
