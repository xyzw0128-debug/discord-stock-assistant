from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class PortfolioChange(Base):
    __tablename__ = "portfolio_changes"
    __table_args__ = (
        CheckConstraint(
            "change_type IN ('NEW_POSITION','SOLD_OUT','SIZE_UP','SIZE_DOWN','AVG_DOWN','AVG_UP')",
            name="ck_portfolio_changes_change_type",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    previous_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("portfolio_snapshots.id"))
    new_snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("portfolio_snapshots.id"))
    ticker: Mapped[str | None] = mapped_column(String(10), ForeignKey("stocks_master.ticker"))
    stock_name: Mapped[str | None] = mapped_column(String(100))
    change_type: Mapped[str | None] = mapped_column(String(20))
    prev_quantity: Mapped[int | None] = mapped_column(Integer)
    new_quantity: Mapped[int | None] = mapped_column(Integer)
    prev_avg_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    new_avg_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    prev_weight_pct: Mapped[float | None] = mapped_column(Numeric(8, 4))
    new_weight_pct: Mapped[float | None] = mapped_column(Numeric(8, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="portfolio_changes")
    previous_snapshot = relationship(
        "PortfolioSnapshot",
        foreign_keys=[previous_snapshot_id],
        back_populates="previous_portfolio_changes",
    )
    new_snapshot = relationship(
        "PortfolioSnapshot",
        foreign_keys=[new_snapshot_id],
        back_populates="new_portfolio_changes",
    )
    stock = relationship("StockMaster", back_populates="portfolio_changes")
