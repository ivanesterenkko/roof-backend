from datetime import datetime
from typing import TYPE_CHECKING, Optional

from constants.subscription import SubscriptionStatus
from sqlalchemy import ForeignKey, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from models.base import Base

if TYPE_CHECKING:
    from models import Company, Tariff


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[Optional[str]]
    status: Mapped[SubscriptionStatus] = mapped_column(
        ENUM(SubscriptionStatus), default=SubscriptionStatus.inactive
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expired_at: Mapped[Optional[datetime]]
    auto_renew: Mapped[bool] = mapped_column(Boolean, server_default="f")

    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    company: Mapped["Company"] = relationship(
        "Company", back_populates="subscriptions"
    )
    tariff_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tariff.id", ondelete="CASCADE"), index=True
    )
    tariff: Mapped["Tariff"] = relationship(
        "Tariff", back_populates="subscriptions"
    )
