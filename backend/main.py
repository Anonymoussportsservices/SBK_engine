import os
import threading
from fastapi import FastAPI
from backend.db import init_db       # adjust import if needed
from backend import mock_feed        # adjust import if needed
from backend import crud, get_db_session  # import your DB helpers

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
@app.on_event("startup")
def on_startup():
    # init DB (create tables if not exist)
    init_db(os.getenv("DATABASE_URL"))

# ----------------------
# Optionally start mock feed in background thread
# ----------------------
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
# Odds endpoint
# ----------------------
@app.get("/api/v1/odds")
def get_odds():
    with get_db_session() as s:
        return crud.list_odds(s)

# ----------------------
# Place bet endpoint
# ----------------------
@app.post("/api/v1/bets")
def place_bet(bet: dict):
    # simple endpoint for MVP testing
    with get_db_session() as s:
        created = crud.create_bet(s, bet)
        return created

# ----------------------
# Example function for preventive check
# ----------------------
def example_function():
    # This is a safe placeholder
    for i in range(3):
        print(f"Loop iteration {i}")
    if True:
        print("If block inside function works correctly")
    else:
        print("Else block inside function works correctly")
