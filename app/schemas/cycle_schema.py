from pydantic import BaseModel
from datetime import date
from typing import Optional


class StartCycleRequest(BaseModel):
    start_date: date


class EndCycleRequest(BaseModel):
    end_date: date


class CycleResponse(BaseModel):
    id: int
    start_date: date
    end_date: Optional[date]
    is_confirmed: bool

    class Config:
        from_attributes = True