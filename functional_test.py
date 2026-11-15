# ============================================
# MAKANLENS MODULE 3
# STEP 18 - FUNCTIONAL TESTING
# ============================================

from profile_service import get_user_profile
from meal_service import get_meal_history, get_daily_nutrition
from wellness_service import get_wellness_history
from feedback_service import generate_feedback
from feedback_history import get_feedback_history
from dashboard_service import get_daily_dashboard
from weekly_trends import get_weekly_trends

# Existing demo user and recorded date
user_id = 1
selected_date = "2026-10-30"

results = []

def run_test(name, function):
    try:
        function()
        results.append((name, "PASS"))
        print(f"[PASS] {name}")
    except Exception as error:
        results.append((name, "FAIL"))
        print(f"[FAIL] {name}: {error}")

# TEST 1: Retrieve user profile
run_test(
    "User Profile",
    lambda: get_user_profile(user_id)
)

# TEST 2: Retrieve meal history
run_test(
    "Meal History",
    lambda: get_meal_history(user_id)
)

# TEST 3: Daily nutrition
run_test(
    "Daily Nutrition",
    lambda: get_daily_nutrition(user_id, selected_date)
)

# TEST 4: Wellness history
run_test(
    "Wellness Tracking",
    lambda: get_wellness_history(user_id)
)

# TEST 5: Personalized feedback
run_test(
    "Personalized Feedback",
    lambda: generate_feedback(user_id, selected_date)
)

# TEST 6: Feedback history
run_test(
    "Feedback History",
    lambda: get_feedback_history(user_id)
)

# TEST 7: Daily dashboard
run_test(
    "Daily Dashboard",
    lambda: get_daily_dashboard(user_id, selected_date)
)

# TEST 8: Weekly trends
run_test(
    "Weekly Trends",
    lambda: get_weekly_trends(user_id, selected_date)
)

# DISPLAY RESULTS
passed = sum(status == "PASS" for _, status in results)

print("\n===== FUNCTIONAL TEST SUMMARY =====")
print("Total Tests:", len(results))
print("Passed:", passed)
print("Failed:", len(results) - passed)
print(f"Pass Rate: {passed / len(results) * 100:.1f}%")
