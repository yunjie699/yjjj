
import sqlite3
from pathlib import Path

# Database location
db_path = Path(__file__).resolve().parent / "makanlens_group.db"

# Check database exists
if not db_path.exists():
    print("Database file not found!")

else:
    conn = sqlite3.connect(db_path)

    print("=== DATABASE TABLES ===")

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()

    for table in tables:
        print(table[0])

    print("\n=== MEAL_LOGS COLUMNS ===")

    columns = conn.execute(
        "PRAGMA table_info(meal_logs)"
    ).fetchall()

    for column in columns:
        print(column)

    print("\n=== FOODS COLUMNS ===")

    columns = conn.execute(
        "PRAGMA table_info(foods)"
    ).fetchall()

    for column in columns:
        print(column)

    print("\n=== FOOD RECORDS ===")

    foods = conn.execute(
        "SELECT food_id, dish_name FROM foods"
    ).fetchall()

    for food in foods:
        print(food)

    print("\n=== PORTION CATEGORIES ===")

    portions = conn.execute(
        "SELECT * FROM portion_categories"
    ).fetchall()

    for portion in portions:
        print(portion)

    print("\n=== USERS ===")

    users = conn.execute(
        "SELECT user_id FROM users"
    ).fetchall()

    for user in users:
        print(user)

    conn.close()

    print("\nDatabase structure check completed!")
