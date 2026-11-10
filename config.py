import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = BASE_DIR / "data" / "questions.json"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DAILY_CHANNEL_ID = int(os.getenv("DAILY_CHANNEL_ID") or 0)
DAILY_POST_TIME = os.getenv("DAILY_POST_TIME") or "18:00"
TIMEZONE = os.getenv("TIMEZONE") or "America/Toronto"


def load_questions():
    """Read the question list fresh each time so edits show up right away."""
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        return json.load(f)