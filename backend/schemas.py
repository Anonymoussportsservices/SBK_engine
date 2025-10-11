# schemas.py - Pydantic models (light)
from pydantic import BaseModel
from typing import Optional




class OddsOut(BaseModel):
id: int
event_id: str
market: str
selection: str
price: float


class Config:
orm_mode = True




class BetCreate(BaseModel):
user_id: Optional[str]
event_id: str
market: str
selection: str
stake: float




class BetOut(BetCreate):
id: int
status: str
odds_at_bet: float


class Config:
orm_mode = True