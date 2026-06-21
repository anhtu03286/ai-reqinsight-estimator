import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Enum as SAEnum, Text, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimestampMixin
import enum


class ResultType(str, enum.Enum):
    clarification = "clarification"
    risk = "risk"
    gap = "gap"
    suggestion = "suggestion"
    test_case = "test_case"


class Severity(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"


class ApprovalStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    document_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    chunk_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("document_chunks.id"), nullable=True)
    result_type: Mapped[ResultType] = mapped_column(SAEnum(ResultType), nullable=False)
    severity: Mapped[Severity | None] = mapped_column(SAEnum(Severity), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    ai_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[ApprovalStatus] = mapped_column(SAEnum(ApprovalStatus), default=ApprovalStatus.pending)
    original_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    edited_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    edited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    persona: Mapped[str | None] = mapped_column(String(50), nullable=True)

    project = relationship("Project", back_populates="analysis_results", lazy="noload")
    approval_records = relationship("ApprovalRecord", back_populates="analysis_result", lazy="noload")
