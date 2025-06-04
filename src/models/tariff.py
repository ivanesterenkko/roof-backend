from typing import TYPE_CHECKING, List
from sqlalchemy import ARRAY, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import Subscription


class Tariff(Base):
    __tablename__ = "tariff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str]
    type: Mapped[str]
    limit_users: Mapped[int]
    price: Mapped[int]
    price_sale: Mapped[int]
    duration: Mapped[int]
    atributes: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="tariff", cascade="all, delete-orphan"
    )
