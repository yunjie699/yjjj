
# ==========================================
# MAKANLENS MODULE 3
# PERSONALISED WELLNESS GOALS
# ==========================================

from datetime import date, timedelta
import sqlite3
from pathlib import Path

from profile_service import get_user_profile

DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


def get_personalised_wellness_goals(user_id, selected_date):

    # STEP 1: Get user profile
    profile = get_user_profile(user_id)

    if not profile:
        return ["Please complete your profile first."]

    age = profile.get("age")
    weight = profile.get("weight_kg")

    if age is None or weight is None or weight <= 0:
        return ["Please enter your age and weight."]

    selected = date.fromisoformat(selected_date)
    week_start = selected - timedelta(days=selected.weekday())

    # STEP 2: Get recorded wellness information
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        daily = conn.execute("""
            SELECT water_ml, sleep_hours, activity_minutes
            FROM wellness_logs
            WHERE user_id = ? AND log_date = ?
            ORDER BY log_id DESC
            LIMIT 1
        """, (user_id, selected_date)).fetchone()

        weekly = conn.execute("""
            SELECT SUM(activity_minutes) AS total_activity
            FROM wellness_logs
            WHERE user_id = ?
              AND log_date BETWEEN ? AND ?
        """, (
            user_id,
            week_start.isoformat(),
            selected_date
        )).fetchone()

    results = []

    # STEP 3: Water goal
    # Illustrative formula only, not a medical requirement
    water_goal = round(weight * 30)
    results.append(
        f"Example daily water goal: {water_goal} ml."
    )

    if daily and daily["water_ml"] is not None:
        water_recorded = daily["water_ml"]
        results.append(
            f"Water recorded: {water_recorded} ml."
        )

        if water_recorded < water_goal:
            results.append(
                "Water tip: Keep track of your drinks today."
            )
        else:
            results.append(
                "Water tip: You reached the example tracking goal."
            )
    else:
        results.append("Water tip: No water record today.")

    # STEP 4: Sleep goal based on age
    if 18 <= age <= 64:
        sleep_min, sleep_max = 7, 9
    elif age >= 65:
        sleep_min, sleep_max = 7, 8
    elif 13 <= age <= 17:
        sleep_min, sleep_max = 8, 10
    else:
        sleep_min, sleep_max = None, None

    if sleep_min is not None:
        results.append(
            f"General sleep goal: {sleep_min}-{sleep_max} hours."
        )

        if daily and daily["sleep_hours"] is not None:
            hours = daily["sleep_hours"]
            results.append(f"Sleep recorded: {hours} hours.")

            if hours < sleep_min:
                results.append(
                    "Sleep tip: Try to get more sleep."
                )
            elif hours <= sleep_max:
                results.append(
                    "Sleep tip: Your sleep is within the general range."
                )
            else:
                results.append(
                    "Sleep tip: Keep a regular sleep schedule."
                )
        else:
            results.append("Sleep tip: No sleep record today.")
    else:
        results.append(
            "Sleep tip: An age-specific goal is not available."
        )

    # STEP 5: Physical activity goal
    if age >= 18:
        activity_goal = 150
        results.append(
            "General activity goal: 150 minutes per week."
        )

        if weekly["total_activity"] is not None:
            activity_recorded = weekly["total_activity"]
            results.append(
                f"Activity recorded this week: "
                f"{activity_recorded:.0f} minutes."
            )

            if activity_recorded < activity_goal:
                results.append(
                    "Activity tip: Keep moving during the week."
                )
            else:
                results.append(
                    "Activity tip: You reached the weekly goal."
                )
        else:
            results.append(
                "Activity tip: No activity recorded this week."
            )
    else:
        results.append(
            "Activity tip: An age-specific activity goal "
            "is not available."
        )

    results.append(
        "These are general wellness tips, not medical advice."
    )

    return results


# STEP 6: Test
if __name__ == "__main__":

    user_id = 1
    selected_date = "2026-10-30"

    print("===== PERSONALISED WELLNESS GOALS =====")

    results = get_personalised_wellness_goals(
        user_id, selected_date
    )

    for number, message in enumerate(results, 1):
        print(f"{number}. {message}")
