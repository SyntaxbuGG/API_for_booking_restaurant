from datetime import datetime, timedelta
from sqlalchemy import exists, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.table import Table
from app.models.reservation import Reservation


# async def check_reservation_conflict(
#     db: AsyncSession,
#     table_id: int,
#     start_time: datetime,
#     duration: int
# ) -> bool:
#     end_time = start_time + timedelta(minutes=duration)

#     stmt = select(Reservation).where(
#         and_(
#             Reservation.table_id == table_id,
#             Reservation.reservation_time < end_time,
#             Reservation.reservation_end_time > start_time

#         )
#     )

#     result = await db.execute(stmt)
#     return result.scalars().first() is not None


async def find_available_table(
    db: AsyncSession, start_time: datetime, duration: int, guest_count: int
) -> int | None:
    # Рассчитываем конечное время брони
    end_time = start_time + timedelta(minutes=duration)
    print(f" Guest count: {guest_count}")

    # Ищем столики с подходящей вместимостью
    stmt = (
        select(Table.id)
        .where(Table.seats >= guest_count)
        .where(
            ~exists().where(
                and_(
                    Reservation.table_id == Table.id,
                    Reservation.reservation_time < end_time,
                    Reservation.reservation_end_time > start_time,
                )
            )
        )
        .order_by(Table.seats.asc())
        .limit(1)
    )
    print(f'Что за запрос {stmt}')
    result = await db.execute(stmt)
    table_id = result.scalar_one_or_none()
    print(f"Found table ID: {table_id}")
    return table_id
