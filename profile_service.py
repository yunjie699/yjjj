import sqlite3
from pathlib import Path
from datetime import datetime

from user_profile import calculate_bmi, calculate_calorie_target

DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


def save_user_profile(user_id, age, gender, height_cm,
                      weight_kg, activity_level):

    # Validate user information
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("Invalid user ID")

    if not 1 <= age <= 120:
        raise ValueError("Invalid age")

    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive")

    # Automatically calculate BMI
    bmi = calculate_bmi(weight_kg, height_cm)

    # Estimate daily maintenance calories
    calorie_target = calculate_calorie_target(
        age, gender, height_cm, weight_kg, activity_level
    )

    # Connect to existing SQLite database
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # Update existing profile or insert new profile
        conn.execute("""
            INSERT INTO user_profiles (
                user_id, age, gender, height_cm,
                weight_kg, activity_level, bmi,
                daily_calorie_target, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                age = excluded.age,
                gender = excluded.gender,
                height_cm = excluded.height_cm,
                weight_kg = excluded.weight_kg,
                activity_level = excluded.activity_level,
                bmi = excluded.bmi,
                daily_calorie_target = excluded.daily_calorie_target,
                updated_at = excluded.updated_at
        """, (
            user_id, age, gender, height_cm,
            weight_kg, activity_level, bmi,
            calorie_target, datetime.now().isoformat()
        ))

    return {
        "user_id": user_id,
        "bmi": bmi,
        "estimated_maintenance_calories": calorie_target
    }


def get_user_profile(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute("""
            SELECT *
            FROM user_profiles
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        return dict(row) if row else None
