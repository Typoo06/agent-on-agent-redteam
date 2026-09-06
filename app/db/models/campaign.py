from datetime import datetime

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, uuid_str
from app.domain.enums import CampaignStatus


class Campaign(TimestampMixin, Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000))
    scenario_id: Mapped[str] = mapped_column(String(36), ForeignKey("scenarios.id"), nullable=False)
    red_agent_profile: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    target_id: Mapped[str] = mapped_column(String(36), ForeignKey("targets.id"), nullable=False)
    judge_profile: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    scope_policy_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("scope_policies.id"), nullable=False
    )
    max_turns: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=20_000, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=900, nullable=False)
    parallelism: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    runs: Mapped[list["CampaignRun"]] = relationship(back_populates="campaign")


class CampaignRun(TimestampMixin, Base):
    __tablename__ = "campaign_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    campaign_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaigns.id"), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(
        String(40), default=CampaignStatus.QUEUED, nullable=False
    )
    started_at: Mapped[datetime | None]
    ended_at: Mapped[datetime | None]
    cancel_requested_at: Mapped[datetime | None]
    failure_reason: Mapped[str | None] = mapped_column(String(2000))
    celery_task_id: Mapped[str | None] = mapped_column(String(255))
    metrics: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)

    campaign: Mapped[Campaign] = relationship(back_populates="runs")
