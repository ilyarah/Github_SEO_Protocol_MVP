# src/seo_protocol/monitor.py
import logging
import sqlite3
from datetime import datetime, timedelta, timezone 



logger = logging.getLogger(__name__)

class Monitor:
    """Simple local storage for historical metrics (SQLite)."""

    def __init__(self, db_path: str = "seo_monitor.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS metrics (
                        repo TEXT NOT NULL,
                        date TEXT NOT NULL,
                        stars INTEGER,
                        forks INTEGER,
                        score REAL,
                        PRIMARY KEY (repo, date)
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")

    def save_current_metrics(self, repo: str, metrics: dict, score: float):
        """Save current snapshot of important metrics."""
        try:
            date_str = datetime.utcnow().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO metrics (repo, date, stars, forks, score)
                    VALUES (?, ?, ?, ?, ?)
                """, (repo, date_str, metrics.get('stars'), metrics.get('forks'), score))
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to save metrics to database: {e}")

    def get_historical_data(self, repo: str, days_back: int = 90) -> list[dict]:
        """Get historical data for the given repository."""
        try:
            cutoff = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT date, stars, forks, score
                    FROM metrics
                    WHERE repo = ? AND date > ?
                    ORDER BY date ASC
                """, (repo, cutoff))

                return [
                    {"date": row[0], "stars": row[1], "forks": row[2], "score": row[3]}
                    for row in cursor.fetchall()
                ]
        except sqlite3.Error as e:
            logger.error(f"Failed to read historical data: {e}")
            return []
