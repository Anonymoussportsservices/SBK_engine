# db.py - SQLAlchemy engine/session + simple init
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./dev.db"


# echo can be turned on for debugging
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()




def init_db(url=None):
    # create tables
    from models import Odds, Bet
    Base.metadata.create_all(bind=engine)




@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
    yield db
    finally:
    db.close()