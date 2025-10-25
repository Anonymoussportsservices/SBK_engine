import json
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from .models import Odds, Bet  # moved to top for clarity

# ----------------------
# List Odds
# ----------------------
def list_odds(db: Session, limit: int = 200) -> List[dict]:
    """
    Returns latest odds up to `limit`.
    """
    odds_list = db.query(Odds).order_by(Odds.updated_at.desc()).limit(limit).all()
    return [serialize_odds(o) for o in odds_list]


def serialize_odds(o: Odds) -> dict:
    """
    Converts an Odds ORM object to dict for API response.
    """
    return {
        "id": o.id,
        "event_id": o.event_id,
        "market": o.market,
        "selection": o.selection,
        "price": o.price,
        "updated_at": o.updated_at.isoformat(),
        "raw": json.loads(o.raw) if isinstance(o.raw, str) else o.raw
    }


# ----------------------
# Create Bet
# ----------------------
def create_bet(db: Session, bet_payload: dict) -> dict:
    b = Bet(
        user_id=bet_payload.get("user_id"),
        event_id=bet_payload.get("event_id"),
        market=bet_payload.get("market"),
        selection=bet_payload.get("selection"),
        stake=float(bet_payload.get("stake", 0)),
        odds_at_bet=float(bet_payload.get("odds_at_bet", 0)),
        raw=json.dumps(bet_payload),
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return {"id": b.id, "status": b.status, "created_at": b.created_at.isoformat()}


# ----------------------
# Upsert Odds
# ----------------------
def upsert_odds(db: Session, o: dict) -> Odds:
    raw_value = o.get("raw") or o
    if isinstance(raw_value, dict):
        raw_value = json.dumps(raw_value)

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
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_data = {
            "event_id": o.get("event_id"),
            "market": o.get("market"),
            "selection": o.get("selection"),
            "price": float(o.get("price", 0)),
            "raw": raw_value,
            "updated_at": o.get("updated_at", datetime.utcnow())
        }
        new = Odds(**new_data)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
