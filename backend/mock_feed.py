import os
import time
import json
import logging
import threading
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend import crud

# ----------------------
# Logging setup
# ----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------
# Control event for graceful stop
# ----------------------
stop_event = threading.Event()

# ----------------------
# Mock feed configuration
# ----------------------
INTERVAL = int(os.getenv("MOCK_FEED_INTERVAL", 30))  # seconds

# Example mock data template
MOCK_ODDS = [
    {"event_id": "MLB_1", "market": "moneyline", "selection": "home", "price": 1.849},
    {"event_id": "MLB_1", "market": "moneyline", "selection": "away", "price": 2.01},
]

# ----------------------
# Start the mock feed
# ----------------------
def start_mock_feed(interval: int = INTERVAL):
    logging.info("[mock_feed] Starting mock feed thread.")
    while not stop_event.is_set():
        db: Session = SessionLocal()
        try:
            for o in MOCK_ODDS:
                try:
                    # upsert handles raw JSON and updated_at
                    crud.upsert_odds(db, o)
                except Exception as e:
                    db.rollback()
                    logging.error(f"[mock_feed] Upsert error: {e}")

        except Exception as e:
            logging.exception(f"[mock_feed] Unexpected error: {e}")
        finally:
            db.close()

        # Wait for interval or exit signal
        stop_event.wait(interval)

    logging.info("[mock_feed] Mock feed stopped.")

# ----------------------
# Stop the mock feed
# ----------------------
def stop_mock_feed():
    stop_event.set()
