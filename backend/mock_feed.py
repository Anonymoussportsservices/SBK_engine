import time
import json
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db import get_db_session


# ----------------------
# CRUD FUNCTIONS
# ----------------------
def list_odds(db: Session, limit: int = 200):
    from .models import Odds  # local import to avoid circular import
    return [o.__dict__ for o in db.query(Odds)
            .order_by(Odds.updated_at.desc())
            .limit(limit)
            .all()]


def create_bet(db: Session, bet_payload: dict):
    from .models import Bet  # local import to avoid circular import
    b = Bet(
        user_id=bet_payload.get("user_id"),
        event_id=bet_payload.get("event_id"),
        market=bet_payload.get("market"),
        selection=bet_payload.get("selection"),
        stake=float(bet_payload.get("stake", 0)),
        odds_at_bet=float(bet_payload.get("odds_at_bet", 0)),
        raw=json.dumps(bet_payload),  # store as JSON string
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return {"id": b.id, "status": b.status, "created_at": str(b.created_at)}


def upsert_odds(db: Session, o: dict):
    from .models import Odds  # local import to avoid circular import
    from json import dumps

    # Ensure 'raw' is a JSON string
    raw_value = o.get("raw") or o
    if isinstance(raw_value, dict):
        raw_value = dumps(raw_value)

    q = db.query(Odds).filter(
        Odds.event_id == o.get("event_id"),
        Odds.market == o.get("market"),
        Odds.selection == o.get("selection")
    )
    existing = q.first()
    if existing:
        existing.price = float(o.get("price", existing.price))
        existing.raw = raw_value
        existing.updated_at = o.get("updated_at", datetime.utcnow())
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_data = {k: v for k, v in o.items() if k in ("event_id", "market", "selection", "price")}
        new_data["raw"] = raw_value
        new_data["updated_at"] = o.get("updated_at", datetime.utcnow())
        new = Odds(**new_data)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new


# ----------------------
# MOCK FEED
# ----------------------
def start_mock_feed(interval=30):
    """
    Starts a continuous mock feed for testing odds.
    Inserts/upserts sample odds every `interval` seconds.
    """
    while True:
        try:
            with get_db_session() as db:
                # Example mock odds
                odds_data = [
                    {"event_id": "MLB_1", "market": "moneyline", "selection": "home", "price": 1.849},
                    {"event_id": "MLB_1", "market": "moneyline", "selection": "away", "price": 2.01},
                ]

                for o in odds_data:
                    # Add updated_at timestamp
                    o["updated_at"] = datetime.utcnow()
                    # Add raw as JSON string
                    o["raw"] = json.dumps(o)

                    try:
                        upsert_odds(db, o)
                    except Exception as e:
                        db.rollback()
                        print(f"[mock_feed] upsert error: {e}")

        except Exception as e:
            print(f"[mock_feed] unexpected error: {e}")

        time.sleep(interval)
