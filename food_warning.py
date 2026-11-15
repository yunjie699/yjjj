
# ==========================================
# MAKANLENS MODULE 3
# SIMPLE FOOD WARNINGS
# ==========================================

import sqlite3
from pathlib import Path

# STEP 1: Connect to the group SQLite database
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# FUNCTION: Generate simple food warnings
def get_food_warnings(user_id, selected_date):

    warnings = []

    # STEP 2: Get recorded food from SQLite
    with sqlite3.connect(DB_PATH) as conn:

        conn.row_factory = sqlite3.Row

        meals = conn.execute("""
            SELECT
                f.dish_name,
                m.calories
            FROM meal_logs AS m
            JOIN foods AS f
                ON m.food_id = f.food_id
            WHERE m.user_id = ?
              AND DATE(m.eaten_at) = ?
        """, (user_id, selected_date)).fetchall()

    # STEP 3: Check whether food records exist
    if not meals:
        return ["No meals recorded for this date."]

    # STEP 4: Check food names
    for meal in meals:

        food = meal["dish_name"].lower()
        calories = meal["calories"]

        # Nasi Lemak
        if "nasi lemak" in food:
            warnings.append(
                "Nasi Lemak: Try less rice and fewer fried side dishes."
            )

        # Roti Canai
        elif "roti canai" in food:
            warnings.append(
                "Roti Canai: Try fewer pieces or choose chapati."
            )

        # Nasi Goreng
        elif "nasi goreng" in food or "fried rice" in food:
            warnings.append(
                "Nasi Goreng: Try less oil and more vegetables."
            )

        # Mee Goreng
        elif "mee goreng" in food or "fried noodles" in food:
            warnings.append(
                "Mee Goreng: Try less oil and more vegetables."
            )

        # Char Kuey Teow
        elif "char kuey teow" in food:
            warnings.append(
                "Char Kuey Teow: Try a smaller portion and less oil."
            )

        # Sweet drinks
        elif "teh tarik" in food or "milo" in food:
            warnings.append(
                "Sweet Drink: Try less sugar or choose plain water."
            )

        # STEP 5: Check high-calorie portions
        # 800 kcal is an example flag, not a medical limit
        if calories is not None and calories >= 800:
            warnings.append(
                "Portion Tip: This meal is high in calories. "
                "Check your portion size."
            )

    # STEP 6: If no warning matches
    if not warnings:
        warnings.append(
            "No specific food tips today. Enjoy balanced meals!"
        )

    # STEP 7: Disclaimer
    warnings.append(
        "These are general food tips, not medical advice."
    )

    return warnings


# ==========================================
# TEST FOOD WARNINGS
# ==========================================

if __name__ == "__main__":

    # Demo user and date
    user_id = 1
    selected_date = "2026-10-30"

    print("===== MAKANLENS FOOD WARNINGS =====")

    results = get_food_warnings(
        user_id, selected_date
    )

    for number, message in enumerate(results, 1):
        print(f"{number}. {message}")
