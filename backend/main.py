import os
import threading
from fastapi import FastAPI
from sqlalchemy import create_engine
from backend.db import get_db_session
from backend.models import Base
from backend import mock_feed  # only mock_feed globally

app = FastAPI()

# ----------------------
# CORS
# ----------------------
origins = os.getenv("CORS_ORIGINS", "*")
if origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in origins.split(",")]


# ----------------------
# Startup event
# ----------------------
def init_db(database_url=None):
    if not database_url:
        database_url = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    engine = create_engine(
        database_url, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)  # create tables


@app.on_event("startup")
def on_startup():
    init_db()
    use_mock = os.getenv("USE_MOCK_FEED", "true").lower() in ("1", "true", "yes")
    if use_mock:
        t = threading.Thread(target=mock_feed.start_mock_feed, daemon=True)
        t.start()


# ----------------------
# Health check endpoint
# ----------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ----------------------
# Root endpoint
# ----------------------
@app.get("/")
def root():
    return {"message": "API is running"}


# ----------------------
# Odds endpoint
# ----------------------
@app.get("/api/v1/odds")
def get_odds():
    from backend import crud  # local import to avoid circular import
    with get_db_session() as s:
        return crud.list_odds(s)


# ----------------------
# Place bet endpoint
# ----------------------
@app.post("/api/v1/bets")
def place_bet(bet: dict):
    from backend import crud  # local import to avoid circular import
    with get_db_session() as s:
        created = crud.create_bet(s, bet)
        return created
