import time
import json
from datetime import datetime
from backend.db import get_db_session
from backend import crud

def start_mock_feed(interval=30):
    while True:
        try:
            with get_db_session() as db:
                # Example mock odds
                odds_data = [
                    {
                        "event_id": "MLB_1",
                        "market": "moneyline",
                        "selection": "home",
                        "price": 1.849,
                    },
                    {
                        "event_id": "MLB_1",
                        "market": "moneyline",
                        "selection": "away",
                        "price": 2.01,
                    },
                ]

                for o in odds_data:
                    # Serialize the dict as JSON string
                    o_raw_json = json.dumps(o)
                    o["raw"] = o_raw_json
                    o["updated_at"] = datetime.utcnow()
                    
                    # Call your CRUD upsert function
                    try:
                        crud.upsert_odds(db, o)
                    except Exception as e:
                        db.rollback()  # rollback on error
                        print(f"[mock_feed] upsert error: {e}")

            time.sleep(interval)
        except Exception as e:
            print(f"[mock_feed] unexpected error: {e}")
            time.sleep(interval)
