# main.py - minimal FastAPI app
import os
import threading
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, get_db_session
import crud
import mock_feed


app = FastAPI(title="MVP Sportsbook API")


# CORS
origins = os.getenv("CORS_ORIGINS", "*")
if origins == "*":
allow_origins = ["*"]
else:
allow_origins = [o.strip() for o in origins.split(",")]


app.add_middleware(
CORSMiddleware,
allow_origins=allow_origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
# init DB (create tables if not exist)
init_db(os.getenv("DATABASE_URL"))


# optionally start mock feed in background thread
use_mock = os.getenv("USE_MOCK_FEED", "true").lower() in ("1","true","yes")
if use_mock:
t = threading.Thread(target=mock_feed.start_mock_feed, daemon=True)
t.start()




@app.get("/health")
def health():
return {"status": "ok"}




@app.get("/api/v1/odds")
def get_odds():
with get_db_session() as s:
return crud.list_odds(s)




@app.post("/api/v1/bets")
def place_bet(bet: dict):
# simple endpoint for MVP testing
with get_db_session() as s:
created = crud.create_bet(s, bet)
return created