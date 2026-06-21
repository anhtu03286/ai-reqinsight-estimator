import uuid
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, TimestampMixin


class RateCard(Base, TimestampMixin):
    __tablename__ = "rate_cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    entries = relationship("RateCardEntry", back_populates="rate_card", lazy="noload", cascade="all, delete-orphan")


class RateCardEntry(Base, TimestampMixin):
    __tablename__ = "rate_card_entries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rate_card_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rate_cards.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    seniority: Mapped[str] = mapped_column(String(50), nullable=False)
    daily_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    rate_card = relationship("RateCard", back_populates="entries", lazy="noload")
