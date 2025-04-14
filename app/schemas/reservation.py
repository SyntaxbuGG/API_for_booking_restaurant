from datetime import datetime
from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int = Field(ge=10)
    guest_count: int = Field(ge=1)


class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    reservation_time: datetime
    guest_count: int
    duration_minutes: int

    class Config:
        from_attributes = True
