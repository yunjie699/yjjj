# ============================================
# MAKANLENS MODULE 3
# STEP 15 - WEEKLY NUTRITION TRENDS
# ============================================

from datetime import date, timedelta
from meal_service import get_daily_nutrition


def get_weekly_trends(user_id, end_date=None):

    # STEP 1: Select the ending date
    if end_date is None:
        end_date = date.today()
    elif isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    weekly_data = []

    # STEP 2: Retrieve the last 7 days
    for i in range(6, -1, -1):

        selected_date = end_date - timedelta(days=i)
        date_text = selected_date.isoformat()

        # Read actual nutrition data from SQLite
        nutrition = get_daily_nutrition(user_id, date_text)

        meals = nutrition.get("total_meals") or 0

        # STEP 3: Store daily totals
        daily_record = {
            "date": date_text,
            "total_meals": meals,
            "calories": (
                nutrition.get("total_calories") or 0
            ) if meals else None,
            "protein_g": nutrition.get("total_protein"),
            "carbs_g": nutrition.get("total_carbs"),
            "fat_g": nutrition.get("total_fat")
        }

        weekly_data.append(daily_record)

    return weekly_data


# ============================================
# TEST WEEKLY NUTRITION TRENDS
# ============================================

if __name__ == "__main__":

    user_id = 1

    # Use this date to include the demo meal
    end_date = "2026-10-31"

    weekly_data = get_weekly_trends(
        user_id,
        end_date
    )

    print("===== MAKANLENS WEEKLY NUTRITION =====")

    for day in weekly_data:
        print("\nDate:", day["date"])
        print("Meals:", day["total_meals"])
        print("Calories:", day["calories"])
        print("Protein:", day["protein_g"])
        print("Carbohydrates:", day["carbs_g"])
        print("Fat:", day["fat_g"])

    # STEP 4: Calculate average calories
    recorded_days = [
        day for day in weekly_data
        if day["total_meals"] > 0
    ]

    if recorded_days:

        average = sum(
            day["calories"] for day in recorded_days
        ) / len(recorded_days)

        print("\n===== WEEKLY SUMMARY =====")
        print("Days with meals logged:", len(recorded_days))
        print("Average logged calories:", round(average, 2))

    else:
        print("\nNo meals recorded during this week.")
