from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.mixins import TimestampMixin, uuid_str
from app.domain.enums import ScopeMode, TargetType


class Target(TimestampMixin, Base):
    __tablename__ = "targets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[TargetType] = mapped_column(String(40), nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(2000))
    model: Mapped[str | None] = mapped_column(String(255))
    config: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ScopePolicy(TimestampMixin, Base):
    __tablename__ = "scope_policies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    mode: Mapped[ScopeMode] = mapped_column(String(40), nullable=False)
    allowed_hosts: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    allowed_cidrs: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    blocked_ports: Mapped[list[int]] = mapped_column(JSON, default=list, nullable=False)
