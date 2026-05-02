from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    source_broker: Mapped[str | None] = mapped_column(String(50))
    total_value: Mapped[float | None] = mapped_column(Numeric(18, 2))
    total_pnl: Mapped[float | None] = mapped_column(Numeric(18, 2))
    cash_balance: Mapped[float | None] = mapped_column(Numeric(18, 2))
    ocr_score: Mapped[int | None] = mapped_column(Integer)
    ocr_method: Mapped[str | None] = mapped_column(String(20))
    raw_ocr_text: Mapped[str | None] = mapped_column(Text)
    image_ref: Mapped[str | None] = mapped_column(Text)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, server_default="false", default=False)

    user = relationship("User", back_populates="portfolio_snapshots")
    holdings = relationship("Holding", back_populates="snapshot", cascade="all, delete-orphan")
    ocr_unmatched_items = relationship(
        "OCRUnmatched", back_populates="snapshot", cascade="all, delete-orphan"
    )
    journal_entries = relationship(
        "JournalEntry", back_populates="snapshot", cascade="all, delete-orphan", single_parent=True
    )
    alerts = relationship(
        "Alert", back_populates="snapshot", cascade="all, delete-orphan", single_parent=True
    )
    upload_logs = relationship(
        "UploadLog", back_populates="snapshot", cascade="all, delete-orphan", single_parent=True
    )
    previous_portfolio_changes: Mapped[List["PortfolioChange"]] = relationship(
        "PortfolioChange",
        foreign_keys="PortfolioChange.previous_snapshot_id",
        back_populates="previous_snapshot",
    )
    new_portfolio_changes: Mapped[List["PortfolioChange"]] = relationship(
        "PortfolioChange",
        foreign_keys="PortfolioChange.new_snapshot_id",
        back_populates="new_snapshot",
    )

    def __repr__(self) -> str:
        return (
            f"PortfolioSnapshot(id={self.id}, user_id={self.user_id}, "
            f"created_at={self.created_at}, source_broker={self.source_broker!r})"
        )
