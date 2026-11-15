# ==========================================
# MAKANLENS - MODULE 3
# MEAL RECORDING AND NUTRITION TRACKING
# ==========================================

# STEP 1: Import the libraries
import sqlite3
from pathlib import Path
from datetime import datetime


# STEP 2: Connect to the existing SQLite database
# This database is shared by all MakanLens modules
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# ==========================================
# FUNCTION 1: SAVE MEAL
# ==========================================

# This function will be called after:
# Module 1 recognises the dish
# Module 2 estimates the calories and nutrients
# The user confirms the dish and portion

def save_meal(user_id, food_id, portion_id,
              calories, protein_g=None,
              carbs_g=None, fat_g=None,
              predicted_dish=None, confidence=None,
              user_corrected=False,
              image_path=None):

    # Check that the calories are valid
    if calories is None or calories < 0:
        raise ValueError("Invalid calorie value")

    # Check that nutrients are not negative
    for value in (protein_g, carbs_g, fat_g):
        if value is not None and value < 0:
            raise ValueError("Invalid nutrient value")

    # Automatically record the current date and time
    eaten_at = datetime.now().isoformat(timespec="seconds")

    # Open the database connection
    with sqlite3.connect(DB_PATH) as conn:

        # Enable foreign key checking
        conn.execute("PRAGMA foreign_keys = ON")

        # Save the confirmed meal into meal_logs
        cursor = conn.execute("""
            INSERT INTO meal_logs (
                user_id,
                food_id,
                portion_id,
                eaten_at,
                image_path,
                predicted_dish,
                confidence,
                user_corrected,
                calories,
                protein_g,
                carbs_g,
                fat_g
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            food_id,
            portion_id,
            eaten_at,
            image_path,
            predicted_dish,
            confidence,
            int(user_corrected),
            calories,
            protein_g,
            carbs_g,
            fat_g
        ))

        # Return the ID of the saved meal
        return cursor.lastrowid


# ==========================================
# FUNCTION 2: VIEW MEAL HISTORY
# ==========================================

# Retrieve the meals recorded by one user
# This data will appear on the Meal History screen

def get_meal_history(user_id):

    # Connect to SQLite
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        # Join meal_logs with foods
        # so the dish name can be displayed
        rows = conn.execute("""
            SELECT
                m.meal_id,
                f.dish_name,
                m.eaten_at,
                m.calories,
                m.protein_g,
                m.carbs_g,
                m.fat_g
            FROM meal_logs AS m
            JOIN foods AS f
                ON m.food_id = f.food_id
            WHERE m.user_id = ?
            ORDER BY m.eaten_at DESC
        """, (user_id,)).fetchall()

        # Return the meal history
        return [dict(row) for row in rows]


# ==========================================
# FUNCTION 3: DAILY NUTRITION SUMMARY
# ==========================================

# Calculate daily calories and macronutrients
# The dashboard will use these results

def get_daily_nutrition(user_id, date):

    # Connect to SQLite
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        # Calculate totals for the selected date
        result = conn.execute("""
            SELECT
                COUNT(*) AS total_meals,
                COALESCE(SUM(calories), 0)
                    AS total_calories,
                SUM(protein_g)
                    AS total_protein,
                SUM(carbs_g)
                    AS total_carbs,
                SUM(fat_g)
                    AS total_fat
            FROM meal_logs
            WHERE user_id = ?
              AND DATE(eaten_at) = ?
        """, (user_id, date)).fetchone()

        # Return the daily nutrition summary
        # NULL nutrient totals mean data is unavailable
        return dict(result)


# ==========================================
# MAIN PROGRAM
# ==========================================

# This section runs only when we execute
# meal_service.py directly in VS Code

if __name__ == "__main__":

    print("================================")
    print(" MAKANLENS MODULE 3 - MEAL SERVICE")
    print("================================")

    # Check that the database exists
    if DB_PATH.exists():
        print("Database found successfully!")
        print("Meal service is ready.")
    else:
        print("ERROR: Database file not found!")
