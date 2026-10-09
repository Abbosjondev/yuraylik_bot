from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str]
    username: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_offer_accepted: Mapped[bool] = mapped_column(Boolean(), server_default="false")
    current_streak: Mapped[int] = mapped_column(default=0)
    highest_streak: Mapped[int] = mapped_column(default=0)
    total_minutes: Mapped[int] = mapped_column(default=0, server_default="0")
    last_activity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notification_time: Mapped[str | None] = mapped_column(String(5))
    is_visible: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    activities: Mapped[list["Activity"]] = relationship(back_populates="user")

    __table_args__ = (
        Index(
            "inx_user_rating",
            text("current_streak DESC"),
            text("highest_streak DESC"),
            text("total_minutes DESC"),
        ),
        Index("idx_user_reminder_active", "notification_time", "is_active"),
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id")
    )
    duration_minutes: Mapped[int]
    record_date: Mapped[date] = mapped_column(Date, server_default=func.current_date())

    user: Mapped[User] = relationship(back_populates="activities")

    __table_args__ = (
        UniqueConstraint("telegram_id", "record_date", name="uq_user_record_date"),
        Index("idx_activity_user_duration", "telegram_id", "duration_minutes"),
    )
