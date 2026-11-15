import sqlite3
from pathlib import Path

# Location of your SQLite database
db_path = Path(__file__).resolve().parent / "makanlens_group.db"

# Check database exists before connecting
if not db_path.exists():
    print("Database file not found!")
else:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    # Check existing tables
    tables = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    print("Database connected successfully!")
    print("Total tables:", len(tables))

    conn.close()
