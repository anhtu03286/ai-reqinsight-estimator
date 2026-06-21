import uuid
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Enum as SAEnum, Text, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimestampMixin
import enum


class WBSItemType(str, enum.Enum):
    epic = "epic"
    story = "story"
    task = "task"


class Complexity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    very_high = "very_high"


class WBSItem(Base, TimestampMixin):
    __tablename__ = "wbs_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("wbs_items.id"), nullable=True)
    item_type: Mapped[WBSItemType] = mapped_column(SAEnum(WBSItemType), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    complexity: Mapped[Complexity | None] = mapped_column(SAEnum(Complexity), nullable=True)
    effort_dev_md: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    effort_qa_md: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    effort_ba_md: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    effort_pm_md: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    risk_buffer_pct: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    historical_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)

    project = relationship("Project", back_populates="wbs_items", lazy="noload")
    children = relationship("WBSItem", lazy="noload", foreign_keys=[parent_id])
