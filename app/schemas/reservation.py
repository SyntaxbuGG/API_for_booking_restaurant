from datetime import datetime
from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int = Field(gt=0)


class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True
