from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.database import get_db
from app.services.reservation import find_available_table

router = APIRouter()


@router.get("/", response_model=list[ReservationResponse])
async def read_reservations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate, db: AsyncSession = Depends(get_db)
):
    # Находим доступный столик автоматически
    table_id = await find_available_table(
        db,
        reservation.reservation_time,
        reservation.duration_minutes,
        reservation.guest_count,
    )

    if not table_id:
        raise HTTPException(
            status_code=400,
            detail="No available tables for the selected time and guest count",
        )

    # Проверяем, что столик существует (на всякий случай)
    table = await db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Создаем бронь с автоматически найденным table_id
    db_reservation = Reservation(
        **reservation.dict(),
        table_id=table_id,  # Используем найденный столик
    )
    db_reservation.set_end_time()
    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation


@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    reservation = await db.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    await db.delete(reservation)
    await db.commit()
    return {"message": "Reservation deleted"}
