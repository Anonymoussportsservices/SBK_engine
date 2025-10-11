from .models import Odds, Bet
from sqlalchemy.orm import Session
import json

def list_odds(db: Session, limit: int = 200):
    return [o.__dict__ for o in db.query(Odds)
            .order_by(Odds.updated_at.desc())
            .limit(limit)
            .all()]

def create_bet(db: Session, bet_payload: dict):
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
    """Simple upsert for Odds by event_id + market + selection."""
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
        existing.updated_at = o.get("updated_at")
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_data = {k: v for k, v in o.items() if k in ("event_id", "market", "selection", "price")}
        new_data["raw"] = raw_value
        new_data["updated_at"] = o.get("updated_at")
        new = Odds(**new_data)
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
