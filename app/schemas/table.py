from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    name: str
    seats: int = Field(gt=0)
    location: str


class TableResponse(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        from_attributes = True
