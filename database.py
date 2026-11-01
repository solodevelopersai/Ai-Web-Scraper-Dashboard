from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class DatabaseManager:
    """Local SQLite storage for privacy-friendly, offline-first data retention."""

    def __init__(self, db_path: str = "data/scraped_data.db") -> None:
        self.db_path = db_path
        self.ensure_parent_directory()

    def ensure_parent_directory(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def initialize_database(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    field TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def insert_scraped_data(self, records: list[dict[str, Any]]) -> int:
        if not records:
            return 0

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.executemany(
                "INSERT INTO scraped_data (field, value) VALUES (?, ?)",
                [(record.get("field", ""), record.get("value", "")) for record in records],
            )
            connection.commit()
            return cursor.rowcount

    def fetch_all(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            rows = cursor.execute("SELECT * FROM scraped_data ORDER BY created_at DESC").fetchall()
            return [dict(row) for row in rows]
