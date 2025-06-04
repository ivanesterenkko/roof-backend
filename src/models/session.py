from typing import TYPE_CHECKING, Optional

from datetime import datetime
from constants.session import DeviceType
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from models.base import Base

if TYPE_CHECKING:
    from models import User


class Session(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    jwt_token: Mapped[str] = mapped_column(unique=True)
    device: Mapped[DeviceType] = mapped_column(
        ENUM(DeviceType), default=DeviceType.desktop
    )
    name: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="sessions")
