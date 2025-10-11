# mock_feed.py - simple file that periodically inserts/updates odds for testing
import time
import random
from db import get_db_session


SAMPLE_EVENTS = [
{"event_id": "MLB_1", "market": "moneyline", "selection": "home", "price": 1.85},
{"event_id": "MLB_1", "market": "moneyline", "selection": "away", "price": 2.05},
{"event_id": "MLB_2", "market": "total", "selection": "over", "price": 1.95},
]




def start_mock_feed(interval_seconds: int = 30):
print("[mock_feed] starting mock feed (interval {}s)".format(interval_seconds))
while True:
with get_db_session() as s:
for e in SAMPLE_EVENTS:
item = dict(e)
# randomize price slightly
delta = random.uniform(-0.05, 0.05)
item["price"] = round(float(item["price"]) + delta, 3)
item["raw"] = item.copy()
# lightweight upsert
from crud import upsert_odds


try:
upsert_odds(s, item)
except Exception as ex:
print("[mock_feed] upsert error:", ex)
time.sleep(interval_seconds)