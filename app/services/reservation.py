from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.reservation import Reservation

async def check_reservation_conflict(
    db: AsyncSession,
    table_id: int,
    start_time: datetime,
    duration: int
) -> bool:
    end_time = start_time + timedelta(minutes=duration)
    
    stmt = select(Reservation).where(
        and_(
            Reservation.table_id == table_id,
            Reservation.reservation_time < end_time,
            Reservation.reservation_time + 
            (Reservation.duration_minutes * timedelta(minutes=1)) > start_time
        )
    )
    
    result = await db.execute(stmt)
    return result.scalars().first() is not None