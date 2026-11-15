# ==========================================
# MAKANLENS MODULE 3
# STEP 10 - DAILY CALORIE TRACKER
# ==========================================

# STEP 1: Import the required libraries
import sqlite3
from pathlib import Path
from datetime import date

# STEP 2: Import the meal summary function
# from the previous meal_service.py file
from meal_service import get_daily_nutrition


# STEP 3: Set the SQLite database location
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# ==========================================
# FUNCTION 1: GET USER CALORIE TARGET
# ==========================================

def get_calorie_target(user_id):

    # Connect to the existing database
    with sqlite3.connect(DB_PATH) as conn:

        # Get the user's daily calorie target
        row = conn.execute("""
            SELECT daily_calorie_target
            FROM user_profiles
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        # Return None if the profile does not exist
        if row is None or row[0] is None:
            return None

        return float(row[0])


# ==========================================
# FUNCTION 2: CALCULATE DAILY PROGRESS
# ==========================================

def calculate_daily_progress(user_id, selected_date):

    # Get calorie target from user_profiles
    target = get_calorie_target(user_id)

    if target is None or target <= 0:
        return None

    # Get daily meal nutrition from meal_logs
    nutrition = get_daily_nutrition(
        user_id, selected_date
    )

    # Calculate total calories consumed
    consumed = float(nutrition["total_calories"])

    # Calculate remaining calories
    remaining = target - consumed

    # Calculate percentage of target consumed
    percentage = (consumed / target) * 100

    # Return results for the dashboard
    return {
        "date": selected_date,
        "target": target,
        "consumed": consumed,
        "remaining": round(remaining, 2),
        "percentage": round(percentage, 2),
        "total_meals": nutrition["total_meals"]
    }


# ==========================================
# FUNCTION 3: PERSONALISED FEEDBACK
# ==========================================

def generate_feedback(progress):

    # Check whether the user has a profile
    if progress is None:
        return "Please complete your health profile."

    # Check whether any meals were recorded
    if progress["total_meals"] == 0:
        return "No meals recorded for this date. Start tracking your meals."

    # Check whether calorie intake exceeds target
    if progress["remaining"] < 0:
        return (
            "Your recorded calorie intake is above "
            "your daily target."
        )

    # Check whether recorded intake is near target
    elif progress["percentage"] >= 90:
        return (
            "Your recorded calorie intake is close "
            "to your daily target."
        )

    # Otherwise, provide general tracking feedback
    else:
        return (
            "Continue recording your meals to "
            "monitor your daily nutrition."
        )


# ==========================================
# MAIN PROGRAM - TEST THE FUNCTIONS
# ==========================================

if __name__ == "__main__":

    # Use the existing demo user in SQLite
    # Later, the interface will supply user_id
    user_id = 1

    # Automatically use today's date
    today = date.today().isoformat()

    # Calculate the user's daily progress
    progress = calculate_daily_progress(
        user_id, today
    )

    print("===================================")
    print(" MAKANLENS - DAILY CALORIE TRACKER")
    print("===================================")

    if progress is None:
        print("User profile or calorie target not found.")

    else:
        print("Date:", progress["date"])
        print("Daily target:", progress["target"], "kcal")
        print("Consumed:", progress["consumed"], "kcal")
        print("Remaining:", progress["remaining"], "kcal")
        print("Progress:", progress["percentage"], "%")
        print("Meals recorded:", progress["total_meals"])

        print("\n===== PERSONALISED FEEDBACK =====")
        print(generate_feedback(progress))
