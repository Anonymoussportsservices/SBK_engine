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
    # convert raw dict to JSON string
    if "raw" in o and isinstance(o["raw"], dict):
        o["raw"] = json.dumps(o["raw"])

    # simple upsert by event_id + market + selection
    q = db.query(Odds).filter(
        Odds.event_id == o.get("event_id"),
        Odds.market == o.get("market"),
        Odds.selection == o.get("selection")
    )
    existing = q.first()
    if existing:
        existing.price = float(o.get("price", existing.price))
        existing.raw = o.get("raw", existing.raw)
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new = Odds(**{k: v for k, v in o.items() if k in ("event_id", "market", "selection", "price", "raw")})
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
