# ============================================
# MAKANLENS MODULE 3
# STEP 14 - DAILY DASHBOARD
# ============================================

from datetime import date

from profile_service import get_user_profile
from meal_service import get_daily_nutrition
from wellness_service import get_wellness_history
from feedback_service import generate_feedback


def get_daily_dashboard(user_id, selected_date=None):

    # STEP 1: Select date
    if selected_date is None:
        selected_date = date.today().isoformat()

    # STEP 2: Read profile from database
    profile = get_user_profile(user_id)

    if profile is None:
        return {
            "error": "User profile not found."
        }

    # STEP 3: Read daily nutrition
    nutrition = get_daily_nutrition(user_id, selected_date)

    calories = nutrition.get("total_calories") or 0
    protein = nutrition.get("total_protein")
    carbs = nutrition.get("total_carbs")
    fat = nutrition.get("total_fat")
    meal_count = nutrition.get("total_meals") or 0

    # STEP 4: Calculate calorie progress
    target = profile.get("daily_calorie_target") or 0

    remaining = target - calories

    progress = (
        round(calories / target * 100, 1)
        if target > 0 else 0
    )

    # STEP 5: Read wellness information
    history = get_wellness_history(user_id)

    wellness = next(
        (
            record for record in history
            if record["log_date"] == selected_date
        ),
        None
    )

    # STEP 6: Generate personalised feedback
    feedback = generate_feedback(user_id, selected_date)

    # STEP 7: Return data for the app interface
    return {
        "user_id": user_id,
        "date": selected_date,
        "bmi": profile.get("bmi"),
        "calorie_target": target,
        "calories_consumed": calories,
        "calories_remaining": remaining,
        "calorie_progress_percent": progress,
        "total_meals": meal_count,
        "protein_g": protein,
        "carbs_g": carbs,
        "fat_g": fat,
        "water_ml": wellness.get("water_ml") if wellness else None,
        "sleep_hours": wellness.get("sleep_hours") if wellness else None,
        "activity_minutes": (
            wellness.get("activity_minutes")
            if wellness else None
        ),
        "feedback": feedback
    }


# ============================================
# TEST THE DASHBOARD
# ============================================

if __name__ == "__main__":

    dashboard = get_daily_dashboard(
        user_id=1,
        selected_date="2026-10-30"
    )

    print("===== MAKANLENS DAILY DASHBOARD =====")

    for key, value in dashboard.items():
        print(key, ":", value)
