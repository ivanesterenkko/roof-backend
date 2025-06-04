from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import (
        User,
        Subscription,
    )


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str]
    inn: Mapped[str] = mapped_column(String, index=True, unique=True)
    ogrn: Mapped[str] = mapped_column(String, index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    users: Mapped[list["User"]] = relationship(
        "User", back_populates="company", cascade="all, delete-orphan"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="company", cascade="all, delete-orphan"
    )
