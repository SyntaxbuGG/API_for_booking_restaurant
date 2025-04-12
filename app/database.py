from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.reservation import Reservation
from app.models.table import Table
from app.base import Base


from typing import AsyncGenerator


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/dbname"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
