# ==========================================
# MAKANLENS MODULE 3
# STEP 13 - PERSONALISED FEEDBACK
# ==========================================

from datetime import date
from profile_service import get_user_profile
from meal_service import get_daily_nutrition
from wellness_service import get_wellness_history


def generate_feedback(user_id, selected_date=None):

    if selected_date is None:
        selected_date = date.today().isoformat()

    profile = get_user_profile(user_id)

    if profile is None:
        return ["Please complete your user profile first."]

    nutrition = get_daily_nutrition(user_id, selected_date)

    feedback = []

    # STEP 1: Check calorie intake
    target = profile.get("daily_calorie_target")
    calories = nutrition.get("total_calories") or 0
    meal_count = nutrition.get("total_meals") or 0

    if meal_count == 0:
        feedback.append(
            "No meals recorded for this date. "
            "Please log your meals to receive calorie feedback."
        )

    elif target and target > 0:

        if calories > target:
            feedback.append(
                "Your recorded calorie intake is above "
                "your estimated daily target."
            )

        elif calories < target * 0.8:
            feedback.append(
                "Your recorded calorie intake is below "
                "80% of your daily target. "
                "Check whether all meals have been logged."
            )

        else:
            feedback.append(
                "Your recorded calorie intake is "
                "within 80-100% of your daily target."
            )

    # STEP 2: Check wellness records
    history = get_wellness_history(user_id)

    daily_wellness = next(
        (
            record for record in history
            if record["log_date"] == selected_date
        ),
        None
    )

    if daily_wellness is None:
        feedback.append(
            "No wellness data recorded for this date."
        )

    else:
        water = daily_wellness.get("water_ml")
        sleep = daily_wellness.get("sleep_hours")
        activity = daily_wellness.get("activity_minutes")

        if water is not None:
            if water < 1500:
                feedback.append(
                    "Your logged water intake is below "
                    "the example tracking threshold of 1500 ml."
                )
            else:
                feedback.append(
                    "Water intake has been recorded."
                )

        if sleep is not None:
            if sleep < 7:
                feedback.append(
                    "Your recorded sleep is below 7 hours. "
                    "Consider maintaining a regular sleep schedule."
                )
            else:
                feedback.append(
                    "Your sleep duration has been recorded."
                )

        if activity is not None:
            feedback.append(
                f"You recorded {activity} minutes "
                "of physical activity."
            )

    feedback.append(
        "This feedback is for general wellness only, "
        "not medical advice."
    )

    return feedback


# Run this file directly to test the function
if __name__ == "__main__":

    user_id = 1
    test_date = "2026-10-30"

    messages = generate_feedback(user_id, test_date)

    print("===== MAKANLENS PERSONALISED FEEDBACK =====")
    print("Date:", test_date)

    for number, message in enumerate(messages, start=1):
        print(f"{number}. {message}")
