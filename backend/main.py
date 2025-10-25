import os
import threading
import requests
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.auth import router as auth_router
from backend import crud, mock_feed
from backend.db import Base, engine, get_db_session
from pydantic import BaseModel

# ----------------------
# Constants
# ----------------------
ODDS_API_BASE_URL = "https://api.the-odds-api.com/v4"
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

# ----------------------
# FastAPI App
# ----------------------
app = FastAPI(title="Sportsbook MVP API", version="1.0.0")

# ----------------------
# CORS
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# OddsAPI Utility Functions
# ----------------------
def fetch_sports():
    try:
        url = f"{ODDS_API_BASE_URL}/sports"
        resp = requests.get(url, params={"apiKey": ODDS_API_KEY})
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports: {e}")

def fetch_odds(sport_key: str, regions: str = "us", odds_format: str = "decimal"):
    try:
        url = f"{ODDS_API_BASE_URL}/sports/{sport_key}/odds"
        params = {"apiKey": ODDS_API_KEY, "regions": regions, "oddsFormat": odds_format}
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching odds: {e}")

# ----------------------
# Startup Event
# ----------------------
@app.on_event("startup")
def on_startup():
    # Initialize DB
    Base.metadata.create_all(bind=engine)

    # Start mock feed if enabled
    use_mock = os.getenv("USE_MOCK_FEED", "true").lower() in ("1", "true", "yes")
    if use_mock:
        t = threading.Thread(target=mock_feed.start_mock_feed, daemon=True)
        t.start()

# ----------------------
# Health Check
# ----------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ----------------------
# Root Endpoint
# ----------------------
@app.get("/")
def root():
    return {"message": "API is running"}

# ----------------------
# Internal Odds (from DB)
# ----------------------
@app.get("/api/v1/odds")
def get_odds(db: Session = Depends(get_db_session)):
    try:
        return crud.list_odds(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# External OddsAPI Endpoints
# ----------------------
@app.get("/api/v1/external/sports")
def list_external_sports():
    return fetch_sports()

@app.get("/api/v1/external/odds")
def list_external_odds(
    sport_key: str = Query(..., description="Sport key from /sports endpoint"),
    regions: str = Query("us", description="Region code (us, uk, eu, au)"),
    odds_format: str = Query("decimal", description="Odds format: decimal, american, fractional")
):
    return fetch_odds(sport_key, regions, odds_format)

# ----------------------
# Place Bet
# ----------------------
class BetCreate(BaseModel):
    user_id: int
    market_id: int
    amount: float
    odds: float

@app.post("/api/v1/bets")
def place_bet(bet: BetCreate, db: Session = Depends(get_db_session)):
    try:
        created = crud.create_bet(db, bet.dict())
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------------
# Include Auth Router
# ----------------------
app.include_router(auth_router, prefix="/api/v1/auth")
