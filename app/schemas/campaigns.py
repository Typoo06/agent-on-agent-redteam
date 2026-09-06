from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.domain.enums import CampaignStatus, ScopeMode, TargetType
from app.schemas.common import ApiModel, JsonObject, now_utc


class ScenarioConfig(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    objective: str = Field(min_length=1, max_length=4000)
    success_criteria: JsonObject = Field(default_factory=dict)
    prohibited_actions: list[str] = Field(default_factory=list)
    metadata: JsonObject = Field(default_factory=dict)


class RedAgentProfile(ApiModel):
    provider: str = Field(default="mock", min_length=1)
    model: str = Field(default="mock-red-agent", min_length=1)
    strategy_set: list[str] = Field(default_factory=list)
    memory_enabled: bool = True
    config: JsonObject = Field(default_factory=dict)


class JudgeProfile(ApiModel):
    provider: str = Field(default="mock", min_length=1)
    model: str = Field(default="mock-judge", min_length=1)
    verifier_names: list[str] = Field(default_factory=list)
    cross_model_adjudication: bool = False
    human_review_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    config: JsonObject = Field(default_factory=dict)


class TargetConfig(ApiModel):
    type: TargetType
    target_id: UUID | None = None
    base_url: str | None = Field(default=None, max_length=2000)
    model: str | None = Field(default=None, max_length=255)
    config: JsonObject = Field(default_factory=dict)


class ScopePolicyConfig(ApiModel):
    mode: ScopeMode = ScopeMode.LOCAL_ONLY
    allowed_hosts: list[str] = Field(default_factory=list)
    allowed_cidrs: list[str] = Field(default_factory=list)
    blocked_ports: list[int] = Field(default_factory=list)


class CampaignCreate(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    scenario: ScenarioConfig
    red_agent: RedAgentProfile = Field(default_factory=RedAgentProfile)
    target: TargetConfig
    judge: JudgeProfile = Field(default_factory=JudgeProfile)
    scope_policy: ScopePolicyConfig = Field(default_factory=ScopePolicyConfig)
    max_turns: int = Field(default=10, ge=1, le=200)
    max_tokens: int = Field(default=20_000, ge=1)
    timeout_seconds: int = Field(default=900, ge=1)
    parallelism: int = Field(default=1, ge=1, le=100)


class CampaignUpdate(ApiModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    scenario: ScenarioConfig | None = None
    red_agent: RedAgentProfile | None = None
    target: TargetConfig | None = None
    judge: JudgeProfile | None = None
    scope_policy: ScopePolicyConfig | None = None
    max_turns: int | None = Field(default=None, ge=1, le=200)
    max_tokens: int | None = Field(default=None, ge=1)
    timeout_seconds: int | None = Field(default=None, ge=1)
    parallelism: int | None = Field(default=None, ge=1, le=100)


class CampaignRead(CampaignCreate):
    id: UUID
    status: CampaignStatus
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @classmethod
    def placeholder(cls, campaign_id: UUID) -> "CampaignRead":
        return cls(
            id=campaign_id,
            status=CampaignStatus.DRAFT,
            name="placeholder",
            scenario=ScenarioConfig(name="placeholder", objective="placeholder"),
            target=TargetConfig(type=TargetType.MOCK_LAB),
        )
