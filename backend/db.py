import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ----------------------
# Database URL
# ----------------------
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./data.db"

# ----------------------
# Engine and session
# ----------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    future=True
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ----------------------
# Initialize DB
# ----------------------
def init_db():
    from backend.models import Odds, Bet  # explicit import
    Base.metadata.create_all(bind=engine)

# ----------------------
# Session helper
# ----------------------
@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

