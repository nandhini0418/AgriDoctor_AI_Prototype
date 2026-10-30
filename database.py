"""
database.py
------------
Handles all SQLite storage for AgriDoctor AI:
  - `diseases` table: static lookup of disease -> remedy info (seeded from data/diseases.csv)
  - `scans` table: history of every leaf scan the app has run

Run this file directly to (re)initialize the database:
    python database.py
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "agridoctor.db"
DISEASES_CSV = BASE_DIR / "data" / "diseases.csv"


def get_connection():
    """Return a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(force_reseed: bool = False):
    """Create tables if they don't exist and seed the diseases table from CSV."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS diseases (
            class_name  TEXT PRIMARY KEY,
            crop        TEXT NOT NULL,
            disease     TEXT NOT NULL,
            severity    TEXT,
            description TEXT,
            remedy      TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            crop        TEXT,
            class_name  TEXT,
            disease     TEXT,
            confidence  REAL,
            source      TEXT
        )
        """
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM diseases")
    count = cur.fetchone()[0]

    if force_reseed or count == 0:
        df = pd.read_csv(DISEASES_CSV)
        df.to_sql("diseases", conn, if_exists="replace", index=False)
        conn.commit()

    conn.close()


def get_disease_info(class_name: str) -> dict:
    """Look up crop/disease/remedy info for a predicted class name."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT crop, disease, severity, description, remedy FROM diseases WHERE class_name = ?",
        (class_name,),
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return {
            "crop": "Unknown",
            "disease": class_name,
            "severity": "Unknown",
            "description": "No information available for this class yet.",
            "remedy": "Add this class to data/diseases.csv to provide guidance.",
        }

    return {
        "crop": row[0],
        "disease": row[1],
        "severity": row[2] if row[2] else "None",
        "description": row[3],
        "remedy": row[4],
    }


def log_scan(crop: str, class_name: str, disease: str, confidence: float, source: str = "upload") -> int:
    """Insert a new scan record into the history table. Returns the new row's id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO scans (timestamp, crop, class_name, disease, confidence, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (datetime.now().isoformat(timespec="seconds"), crop, class_name, disease, confidence, source),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def fetch_history(limit: int = 200) -> pd.DataFrame:
    """Return scan history as a DataFrame, most recent first."""
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM scans ORDER BY id DESC LIMIT ?", conn, params=(limit,)
    )
    conn.close()
    return df


def clear_history():
    """Wipe scan history (used by the 'reset demo data' button in the app)."""
    conn = get_connection()
    conn.execute("DELETE FROM scans")
    conn.commit()
    conn.close()


def delete_scan(scan_id: int):
    """Delete a single scan entry by its id."""
    conn = get_connection()
    conn.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    conn.commit()
    conn.close()


def get_previous_scan(crop: str, before_id: int = None):
    """
    Return the most recent prior scan for the given crop (for the
    'compare with last scan' feature), or None if there isn't one.
    `before_id` excludes the scan that was just logged, so comparing
    doesn't just compare a scan against itself.
    """
    conn = get_connection()
    cur = conn.cursor()
    if before_id is not None:
        cur.execute(
            """
            SELECT id, timestamp, disease, confidence, class_name FROM scans
            WHERE crop = ? AND id < ?
            ORDER BY id DESC LIMIT 1
            """,
            (crop, before_id),
        )
    else:
        cur.execute(
            """
            SELECT id, timestamp, disease, confidence, class_name FROM scans
            WHERE crop = ?
            ORDER BY id DESC LIMIT 1
            """,
            (crop,),
        )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return {"id": row[0], "timestamp": row[1], "disease": row[2], "confidence": row[3], "class_name": row[4]}


if __name__ == "__main__":
    init_db(force_reseed=True)
    print(f"Database initialized at {DB_PATH}")
    conn = get_connection()
    n = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
    conn.close()
    print(f"Seeded {n} disease/remedy records.")
