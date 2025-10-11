# models.py - minimal models for Odds + Bet
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from db import Base




class Odds(Base):
__tablename__ = "odds"
id = Column(Integer, primary_key=True, index=True)
event_id = Column(String, index=True)
market = Column(String, index=True)
selection = Column(String)
price = Column(Float)
raw = Column(JSON, nullable=True)
updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())




class Bet(Base):
__tablename__ = "bets"
id = Column(Integer, primary_key=True, index=True)
user_id = Column(String, index=True, nullable=True)
event_id = Column(String)
market = Column(String)
selection = Column(String)
stake = Column(Float)
odds_at_bet = Column(Float)
status = Column(String, default="pending")
raw = Column(JSON, nullable=True)
created_at = Column(DateTime(timezone=True), server_default=func.now())