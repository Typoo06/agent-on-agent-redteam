from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, uuid_str
from app.domain.enums import MessageRole


class Turn(TimestampMixin, Base):
    __tablename__ = "turns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    turn_index: Mapped[int] = mapped_column(Integer, nullable=False)
    strategy: Mapped[str | None] = mapped_column(String(255))
    refusal_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    token_usage: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    latency_ms: Mapped[int | None]


class Message(TimestampMixin, Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turns.id"))
    role: Mapped[MessageRole] = mapped_column(String(40), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str | None] = mapped_column(String(100))
    model: Mapped[str | None] = mapped_column(String(255))
    raw: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)


class ToolTrace(TimestampMixin, Base):
    __tablename__ = "tool_traces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    turn_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("turns.id"))
    tool_name: Mapped[str] = mapped_column(String(255), nullable=False)
    input: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    output: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    latency_ms: Mapped[int | None]
    error: Mapped[str | None] = mapped_column(String(2000))


class TelemetryEvent(TimestampMixin, Base):
    __tablename__ = "telemetry_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
