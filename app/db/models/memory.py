from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, uuid_str
from app.domain.enums import AgentType, MemoryType


class MemoryItem(TimestampMixin, Base):
    __tablename__ = "memory_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("campaign_runs.id"), nullable=False)
    agent_type: Mapped[AgentType] = mapped_column(String(40), nullable=False)
    memory_type: Mapped[MemoryType] = mapped_column(String(40), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict[str, object]] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )
