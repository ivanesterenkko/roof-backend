from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from constants.user import UserRole
from models.base import Base

if TYPE_CHECKING:
    from models import (
        Company,
        Session,
        # Project,
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fio: Mapped[str]
    login: Mapped[str] = mapped_column(String, index=True)
    hashed_password: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(String, index=True)
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean, server_default="f"
    )
    role: Mapped[UserRole] = mapped_column(
        ENUM(UserRole), default=UserRole.admin
    )
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="f")
    company_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    company: Mapped["Company"] = relationship(
        "Company", back_populates="users"
    )
    sessions: Mapped[list["Session"]] = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"Пользователь {self.fio}"
