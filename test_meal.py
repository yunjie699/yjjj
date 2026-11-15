# ======================================
# MAKANLENS MODULE 3
# STEP 8 - TEST MEAL HISTORY
# ======================================

# Import the meal service functions
from meal_service import get_meal_history, get_daily_nutrition
from datetime import date

# Use the existing demo user
user_id = 1

# Get meals saved in the database
meals = get_meal_history(user_id)

print("===== MEAL HISTORY =====")

if meals:
    for meal in meals:
        print(meal)
else:
    print("No meals recorded yet.")

# Get today's nutrition summary
today = date.today().isoformat()
summary = get_daily_nutrition(user_id, today)

print("\n===== DAILY NUTRITION =====")
print("Date:", today)
print("Total meals:", summary["total_meals"])
print("Total calories:", summary["total_calories"])
print("Total protein:", summary["total_protein"])
print("Total carbohydrates:", summary["total_carbs"])
print("Total fat:", summary["total_fat"])
