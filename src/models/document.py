import uuid
from sqlalchemy import String, ForeignKey, Enum as SAEnum, Boolean, BigInteger
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimestampMixin
import enum


class DocumentFormat(str, enum.Enum):
    pdf = "pdf"
    docx = "docx"
    doc = "doc"
    md = "md"
    txt = "txt"
    xlsx = "xlsx"
    xls = "xls"
    csv = "csv"


class ParseStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    failed = "failed"


ALLOWED_FORMATS = {fmt.value for fmt in DocumentFormat}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50MB


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    format: Mapped[DocumentFormat] = mapped_column(SAEnum(DocumentFormat), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    version_label: Mapped[str | None] = mapped_column(String(50), nullable=True)
    language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    ocr_applied: Mapped[bool] = mapped_column(Boolean, default=False)
    parse_status: Mapped[ParseStatus] = mapped_column(SAEnum(ParseStatus), default=ParseStatus.pending)
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    project = relationship("Project", back_populates="documents", lazy="noload")
    chunks = relationship("DocumentChunk", back_populates="document", lazy="noload")
