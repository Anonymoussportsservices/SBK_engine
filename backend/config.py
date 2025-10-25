"""
App Configuration (Cloud + Local)
---------------------------------
Centralized environment configuration for the Sportsbook MVP.
Loads from .env during local development, while in production
values come directly from the cloud environment variables.
"""

import os
from dotenv import load_dotenv

# ----------------------
# Load .env only in local/dev environments
# ----------------------
if os.getenv("ENV", "local") == "local":
    load_dotenv()

# ----------------------
# Core configuration
# ----------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
USE_MOCK_FEED = os.getenv("USE_MOCK_FEED", "true").lower() in ("1", "true", "yes")
MOCK_FEED_INTERVAL = int(os.getenv("MOCK_FEED_INTERVAL", 30))

# ----------------------
# External API Keys
# ----------------------
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

# ----------------------
# Sanity checks (optional for safety)
# ----------------------
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing — please set it in your environment.")
if not ODDS_API_KEY:
    print("⚠️ Warning: ODDS_API_KEY not found. External odds API will not function.")

