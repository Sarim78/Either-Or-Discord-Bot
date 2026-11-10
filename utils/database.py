import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "votes.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(_connect()) as conn:
        with conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS polls (
                    message_id INTEGER PRIMARY KEY,
                    channel_id INTEGER NOT NULL,
                    option_a   TEXT NOT NULL,
                    option_b   TEXT NOT NULL,
                    daily      INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS votes (
                    message_id INTEGER NOT NULL,
                    user_id    INTEGER NOT NULL,
                    choice     TEXT NOT NULL CHECK (choice IN ('a', 'b')),
                    PRIMARY KEY (message_id, user_id)
                );
                """
            )


def create_poll(message_id, channel_id, option_a, option_b, daily=False) -> None:
    with closing(_connect()) as conn:
        with conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO polls
                    (message_id, channel_id, option_a, option_b, daily)
                VALUES (?, ?, ?, ?, ?)
                """,
                (message_id, channel_id, option_a, option_b, int(daily)),
            )


def get_poll(message_id):
    with closing(_connect()) as conn:
        return conn.execute(
            "SELECT * FROM polls WHERE message_id = ?", (message_id,)
        ).fetchone()


def add_vote(message_id, user_id, choice) -> bool:
    """Save a vote. Returns False if this user already voted on this poll."""
    with closing(_connect()) as conn:
        with conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO votes (message_id, user_id, choice)
                VALUES (?, ?, ?)
                """,
                (message_id, user_id, choice),
            )
            return cursor.rowcount == 1


def get_user_vote(message_id, user_id):
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT choice FROM votes WHERE message_id = ? AND user_id = ?",
            (message_id, user_id),
        ).fetchone()
        return row["choice"] if row else None


def get_counts(message_id):
    """Return (votes_for_a, votes_for_b)."""
    with closing(_connect()) as conn:
        rows = conn.execute(
            """
            SELECT choice, COUNT(*) AS total
            FROM votes
            WHERE message_id = ?
            GROUP BY choice
            """,
            (message_id,),
        ).fetchall()
    counts = {row["choice"]: row["total"] for row in rows}
    return counts.get("a", 0), counts.get("b", 0)