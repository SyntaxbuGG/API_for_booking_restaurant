from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.database import get_db
from app.services.reservation import check_reservation_conflict

router = APIRouter()


@router.get("/", response_model=list[ReservationResponse])
async def read_reservations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Reservation))
    return result.scalars().all()


@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate, db: AsyncSession = Depends(get_db)
):
    # Check table exists
    table = await db.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Check time conflict (добавляем await)
    if await check_reservation_conflict(
        db,
        reservation.table_id,
        reservation.reservation_time,
        reservation.duration_minutes,
    ):
        raise HTTPException(status_code=400, detail="Time slot already booked")

    # Create reservation
    db_reservation = Reservation(**reservation.dict())
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
