"""
Database setup for Sportsbook MVP (cloud-ready)
------------------------------------------------
Handles SQLAlchemy engine creation, session management, and Base declaration.
Automatically loads DATABASE_URL from backend.config.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from backend.config import DATABASE_URL

# ----------------------
# SQLAlchemy engine & session
# ----------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    future=True  # SQLAlchemy 2.0 style
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ----------------------
# FastAPI DB dependency
# ----------------------
def get_db_session() -> Session:
    """
    FastAPI dependency that provides a DB session and closes it automatically.
    Usage: db: Session = Depends(get_db_session)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------
# Optional: Initialize tables
# ----------------------
def init_db():
    """
    Initialize all tables in the database. 
    Use only for local testing or initial setup.
    """
    import backend.models  # ensures models are loaded
    Base.metadata.create_all(bind=engine)
