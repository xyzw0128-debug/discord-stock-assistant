from datetime import datetime

from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discord_user_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    portfolio_snapshots = relationship(
        "PortfolioSnapshot", back_populates="user", cascade="all, delete-orphan"
    )
    portfolio_changes = relationship(
        "PortfolioChange", back_populates="user", cascade="all, delete-orphan", single_parent=True
    )
    journal_entries = relationship(
        "JournalEntry", back_populates="user", cascade="all, delete-orphan", single_parent=True
    )
    alerts = relationship(
        "Alert", back_populates="user", cascade="all, delete-orphan", single_parent=True
    )
    preference = relationship(
        "UserPreference", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    upload_logs = relationship(
        "UploadLog", back_populates="user", cascade="all, delete-orphan", single_parent=True
    )
