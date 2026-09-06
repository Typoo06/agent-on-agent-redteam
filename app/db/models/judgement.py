from sqlalchemy import JSON, Boolean, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, uuid_str
from app.domain.enums import JudgementStatus


class Judgement(TimestampMixin, Base):
    __tablename__ = "judgements"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    status: Mapped[JudgementStatus] = mapped_column(String(40), nullable=False)
    vulnerability_type: Mapped[str | None] = mapped_column(String(255))
    confidence: Mapped[float | None] = mapped_column(Float)
    rationale: Mapped[str | None] = mapped_column(Text)
    evidence_refs: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class VerifierResult(TimestampMixin, Base):
    __tablename__ = "verifier_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    verifier_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[JudgementStatus] = mapped_column(String(40), nullable=False)
    score: Mapped[float | None] = mapped_column(Float)
    evidence: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    details: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
