from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    preferred_broker: Mapped[str | None] = mapped_column(String(50), nullable=True)
    concentration_alert_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        server_default="30.00",
    )
    cash_alert_pct: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        server_default="10.00",
    )
    notify_on_upload: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="true",
    )
    language: Mapped[str] = mapped_column(String(10), nullable=False, server_default="ko")
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user = relationship("User", back_populates="preference", uselist=False)
