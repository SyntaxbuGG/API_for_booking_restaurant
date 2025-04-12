from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.table import Table
from app.schemas.table import TableCreate, TableResponse
from app.database import get_db
from app.models.reservation import Reservation

router = APIRouter()


@router.get("/", response_model=list[TableResponse])
async def read_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Table))
    return result.scalars().all()


@router.post("/", response_model=TableResponse)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table


@router.delete("/{table_id}")
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):
    table = await db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Проверка на существующие брони

    result = await db.execute(
        select(func.count()).where(Reservation.table_id == table_id)
    )
    if result.scalar() > 0:
        raise HTTPException(status_code=400, detail="Table has active reservations")

    await db.delete(table)
    await db.commit()
    return {"message": "Table deleted"}
