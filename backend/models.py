import time
import json
from datetime import datetime
from backend.db import get_db_session
from backend import crud

def start_mock_feed(interval=30):
    """
    Continuous mock feed for testing odds.
    Inserts/upserts sample odds every `interval` seconds.
    """
    while True:
        try:
            with get_db_session() as db:
                odds_data = [
                    {"event_id": "MLB_1", "market": "moneyline", "selection": "home", "price": 1.849},
                    {"event_id": "MLB_1", "market": "moneyline", "selection": "away", "price": 2.01},
                ]
                for o in odds_data:
                    o["raw"] = json.dumps(o)
                    o["updated_at"] = datetime.utcnow()
                    try:
                        crud.upsert_odds(db, o)
                    except Exception as e:
                        db.rollback()
                        print(f"[mock_feed] upsert error: {e}")
        except Exception as e:
            print(f"[mock_feed] unexpected error: {e}")
        time.sleep(interval)
