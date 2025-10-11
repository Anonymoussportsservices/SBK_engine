from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.db import Base
import datetime

class Odds(Base):
    __tablename__ = "odds"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    market = Column(String)
    selection = Column(String)
    price = Column(Float)
    raw = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    event_id = Column(String)
    market = Column(String)
    selection = Column(String)
    stake = Column(Float)
    odds = Column(Float)
    result = Column(String)
    placed_at = Column(DateTime, default=datetime.datetime.utcnow)
