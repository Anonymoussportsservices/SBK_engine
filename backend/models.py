from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from backend.db import Base
from datetime import datetime

Base = declarative_base()  # ✅ must come first and no circular imports
# backend/models.py


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Odds(Base):
    __tablename__ = "odds"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    market = Column(String)
    selection = Column(String)
    price = Column(Float)
    raw = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    event_id = Column(String)
    market = Column(String)
    selection = Column(String)
    stake = Column(Float)
    odds_at_bet = Column(Float)
    raw = Column(JSON)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
