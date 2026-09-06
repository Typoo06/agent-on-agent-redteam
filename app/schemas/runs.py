from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.domain.enums import CampaignStatus, JudgementStatus, MessageRole
from app.schemas.common import ApiModel, JsonObject, now_utc


class CampaignRunCreate(ApiModel):
    idempotency_key: str | None = Field(default=None, max_length=255)
    overrides: JsonObject = Field(default_factory=dict)


class CampaignRunRead(ApiModel):
    id: UUID
    campaign_id: UUID
    status: CampaignStatus
    started_at: datetime | None = None
    ended_at: datetime | None = None
    cancel_requested_at: datetime | None = None
    failure_reason: str | None = None
    celery_task_id: str | None = None
    metrics: JsonObject = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @classmethod
    def placeholder(
        cls, run_id: UUID, status: CampaignStatus = CampaignStatus.QUEUED
    ) -> "CampaignRunRead":
        return cls(id=run_id, campaign_id=run_id, status=status)


class RunActionResponse(ApiModel):
    run_id: UUID
    accepted: bool
    status: CampaignStatus


class MessageRead(ApiModel):
    id: UUID
    role: MessageRole
    content: str
    metadata: JsonObject = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=now_utc)


class TurnRead(ApiModel):
    id: UUID
    turn_index: int
    red_message: MessageRead | None = None
    target_message: MessageRead | None = None
    strategy: str | None = None
    refusal_detected: bool = False
    token_usage: JsonObject = Field(default_factory=dict)
    latency_ms: int | None = None


class TranscriptRead(ApiModel):
    run_id: UUID
    turns: list[TurnRead]


class JudgementRead(ApiModel):
    run_id: UUID
    status: JudgementStatus | None = None
    vulnerability_type: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    rationale: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = False


class RunMetricsRead(ApiModel):
    run_id: UUID
    total_turns: int = 0
    total_tokens: int = 0
    refusal_count: int = 0
    latency_ms_p50: int | None = None
    latency_ms_p95: int | None = None
    cost_estimate_usd: float | None = None
