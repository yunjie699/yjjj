import sqlite3
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "makanlens_group.db"
JSON_PATH = BASE_DIR / "makanlens_latest_meal.json"

USER_ID = 1


def save_module2_meal():
    if not JSON_PATH.exists():
        print("ERROR: Module 2 JSON file not found.")
        return

    if not DB_PATH.exists():
        print("ERROR: Database not found.")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        meal = json.load(file)

    # Module 2 JSON may use these field names
    food_name = meal.get("food_name", meal.get("dish_name"))
    calories = meal.get("calories", meal.get("calories_kcal"))
    protein = meal.get("protein", meal.get("protein_g"))
    carbs = meal.get("carbs", meal.get("carbs_g"))
    fat = meal.get("fat", meal.get("fat_g"))

    if not food_name or calories is None:
        print("ERROR: Food name or calories missing.")
        return

    portion_name = meal.get("portion_category", "Medium")
    eaten_at = meal.get("eaten_at") or datetime.now().isoformat(
        timespec="seconds"
    )

    conn = sqlite3.connect(DB_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        food = conn.execute(
            """
            SELECT food_id
            FROM foods
            WHERE LOWER(dish_name) = LOWER(?)
            """,
            (food_name,)
        ).fetchone()

        if not food:
            print("ERROR: Food not found in database:", food_name)
            return

        portion = conn.execute(
            """
            SELECT portion_id
            FROM portion_categories
            WHERE LOWER(label) = LOWER(?)
            """,
            (portion_name,)
        ).fetchone()

        if not portion:
            print("ERROR: Portion not found:", portion_name)
            return

        # Save the received nutrition values
        cursor = conn.execute(
            """
            INSERT INTO meal_logs (
                user_id,
                food_id,
                portion_id,
                eaten_at,
                predicted_dish,
                calories,
                protein_g,
                carbs_g,
                fat_g
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                USER_ID,
                food[0],
                portion[0],
                eaten_at,
                food_name,
                calories,
                protein,
                carbs,
                fat
            )
        )

        conn.commit()

        print("=== MODULE 2 TO MODULE 3 ===")
        print("Meal saved successfully!")
        print("Meal ID:", cursor.lastrowid)
        print("Food:", food_name)
        print("Portion:", portion_name)
        print("Calories:", calories, "kcal")
        print("Protein:", protein, "g")
        print("Carbohydrates:", carbs, "g")
        print("Fat:", fat, "g")

    except sqlite3.Error as error:
        conn.rollback()
        print("Database error:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    save_module2_meal()
