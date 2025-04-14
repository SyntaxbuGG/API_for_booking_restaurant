from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base


# Вызываем модел для аннотаций
# Это лучший способ, если ты хочешь избежать циклического импорта:
if TYPE_CHECKING:
    from app.models.reservation import Reservation


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    seats: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="table", cascade="all"
    )
