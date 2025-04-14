from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from annotated_types import T

from app.base import Base

from sqlalchemy import ForeignKey, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime


# Вызываем модел для аннотаций
# Это лучший способ, если ты хочешь избежать циклического импорта:
if TYPE_CHECKING:
    from app.models.table import Table


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    reservation_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    duration_minutes: Mapped[int] = mapped_column(default=10, nullable=False)
    guest_count: Mapped[int] = mapped_column(default=1)
    table: Mapped["Table"] = relationship(back_populates="reservations")
    reservation_end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def set_end_time(self):
        self.reservation_end_time = self.reservation_time + timedelta(
            minutes=self.duration_minutes
        )
