import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent / "makanlens_group.db"

conn = sqlite3.connect(db_path)

columns = conn.execute(
    "PRAGMA table_info(user_profiles)"
).fetchall()

print("===== USER PROFILES TABLE =====")

if columns:
    for column in columns:
        print(column[1], "-", column[2])
else:
    print("Table user_profiles not found!")

conn.close()
