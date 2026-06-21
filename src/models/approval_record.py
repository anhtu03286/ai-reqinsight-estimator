import uuid
from sqlalchemy import String, ForeignKey, Enum as SAEnum, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimestampMixin
import enum


class ApprovalAction(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"


class ApprovalRecord(Base, TimestampMixin):
    __tablename__ = "approval_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analysis_results.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    action: Mapped[ApprovalAction] = mapped_column(SAEnum(ApprovalAction), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    analysis_result = relationship("AnalysisResult", back_populates="approval_records", lazy="noload")
