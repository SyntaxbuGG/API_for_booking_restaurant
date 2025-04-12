from fastapi import FastAPI
from app.routers import tables, reservations

app = FastAPI()

app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
