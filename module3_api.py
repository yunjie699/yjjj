
# ==========================================
# MAKANLENS - MODULE 3 API
# PERSONALISED HEALTH MONITORING
# ==========================================

# STEP 1: Import existing functions

from profile_service import get_user_profile
from meal_service import get_meal_history
from wellness_service import get_wellness_history
from dashboard_service import get_daily_dashboard
from weekly_trends import get_weekly_trends
from feedback_service import generate_feedback
from feedback_history import get_feedback_history
from diet_recommendation import get_diet_recommendations
from food_warning import get_food_warnings

from wellness_prediction import (
    get_wellness_insights,
    predict_weight_trend
)

# NEW: Personalised Wellness Goals
from wellness_goals import get_personalised_wellness_goals


# ==========================================
# STEP 2: MODULE 3 FUNCTIONS
# ==========================================

def show_profile(user_id):
    return get_user_profile(user_id)


def show_dashboard(user_id, selected_date):
    return get_daily_dashboard(user_id, selected_date)


def show_meals(user_id):
    return get_meal_history(user_id)


def show_wellness(user_id):
    return get_wellness_history(user_id)


def show_weekly_trends(user_id, selected_date):
    return get_weekly_trends(user_id, selected_date)


def show_feedback(user_id, selected_date):
    return generate_feedback(user_id, selected_date)


def show_feedback_history(user_id):
    return get_feedback_history(user_id)


def show_diet_recommendations(user_id, selected_date):
    return get_diet_recommendations(user_id, selected_date)


def show_food_warnings(user_id, selected_date):
    return get_food_warnings(user_id, selected_date)


def show_wellness_insights(user_id):
    return get_wellness_insights(user_id)


def show_weight_prediction(user_id):
    return predict_weight_trend(user_id)


# NEW FUNCTION
def show_wellness_goals(user_id, selected_date):
    return get_personalised_wellness_goals(
        user_id, selected_date
    )


# ==========================================
# STEP 3: DISPLAY RESULTS
# ==========================================

if __name__ == "__main__":

    user_id = 1
    selected_date = "2026-11-14"

    print("=" * 50)
    print("       MAKANLENS - MODULE 3")
    print("   PERSONALISED HEALTH MONITORING")
    print("=" * 50)

    # SECTION 1
    print("\n1. USER PROFILE")
    print(show_profile(user_id))

    # SECTION 2
    print("\n2. DAILY DASHBOARD")
    print(show_dashboard(user_id, selected_date))

    # SECTION 3
    print("\n3. MEAL HISTORY")
    print(show_meals(user_id))

    # SECTION 4
    print("\n4. WELLNESS HISTORY")
    print(show_wellness(user_id))

    # SECTION 5
    print("\n5. WEEKLY NUTRITION TRENDS")
    print(show_weekly_trends(user_id, selected_date))

    # SECTION 6
    print("\n6. PERSONALISED FEEDBACK")
    print(show_feedback(user_id, selected_date))

    # SECTION 7
    print("\n7. FEEDBACK HISTORY")
    print(show_feedback_history(user_id))

    # SECTION 8
    print("\n8. DIET RECOMMENDATIONS")
    for number, message in enumerate(
        show_diet_recommendations(user_id, selected_date), 1
    ):
        print(f"{number}. {message}")

    # SECTION 9
    print("\n9. FOOD WARNINGS")
    for number, message in enumerate(
        show_food_warnings(user_id, selected_date), 1
    ):
        print(f"{number}. {message}")

    # SECTION 10
    print("\n10. WELLNESS INSIGHTS")
    for number, message in enumerate(
        show_wellness_insights(user_id), 1
    ):
        print(f"{number}. {message}")

    # SECTION 11
    print("\n11. WEIGHT TREND PREDICTION")
    print(show_weight_prediction(user_id))

    # SECTION 12 - NEW
    print("\n12. PERSONALISED WELLNESS GOALS")

    for number, message in enumerate(
        show_wellness_goals(user_id, selected_date), 1
    ):
        print(f"{number}. {message}")

    print("\n" + "=" * 50)
    print("       MODULE 3 TEST COMPLETED")
    print("=" * 50)
