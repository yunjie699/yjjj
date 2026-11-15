
# ==========================================
# MAKANLENS MODULE 3
# SIMPLE DIET RECOMMENDATIONS
# ==========================================

# Import user profile and nutrition functions
from profile_service import get_user_profile
from meal_service import get_daily_nutrition


# FUNCTION: Generate simple diet recommendations
def get_diet_recommendations(user_id, selected_date):

    # STEP 1: Get user information from SQLite
    profile = get_user_profile(user_id)

    if profile is None:
        return ["Please complete your profile first."]

    # STEP 2: Get recorded meals and nutrition
    nutrition = get_daily_nutrition(user_id, selected_date)

    if not nutrition or nutrition.get("total_meals", 0) == 0:
        return ["Please record your meals to get food tips."]

    recommendations = []

    # STEP 3: Get BMI and calories
    bmi = profile.get("bmi")
    target = profile.get("daily_calorie_target")
    calories = nutrition.get("total_calories") or 0

    # STEP 4: Simple BMI recommendations
    # BMI alone cannot determine which nutrients to reduce
    if bmi is not None:

        if bmi < 18.5:
            recommendations.append(
                "Try eating regular, balanced meals."
            )

        elif bmi < 25:
            recommendations.append(
                "Keep eating balanced meals and stay active."
            )

        else:
            recommendations.append(
                "Try smaller portions and balanced meals."
            )

    # STEP 5: Simple calorie recommendations
    if target is not None and target > 0:

        if calories > target:
            recommendations.append(
                "You have logged more calories than your daily goal."
            )

        else:
            recommendations.append(
                "Keep tracking your meals to check your calories."
            )

    # STEP 6: Check recorded nutrients
    # Use the correct keys returned by meal_service.py
    protein = nutrition.get("total_protein")
    carbs = nutrition.get("total_carbs")
    fat = nutrition.get("total_fat")

    # Only check nutrients when all values are available
    if all(v is not None for v in (protein, carbs, fat)):

        # Calculate energy from each nutrient
        total_energy = protein * 4 + carbs * 4 + fat * 9

        if total_energy > 0:

            protein_percent = protein * 4 / total_energy * 100
            carbs_percent = carbs * 4 / total_energy * 100
            fat_percent = fat * 9 / total_energy * 100

            # Simple fat recommendation
            if fat_percent > 35:
                recommendations.append(
                    "Try eating less fried and oily food."
                )

            # Simple carbohydrate recommendation
            if carbs_percent > 65:
                recommendations.append(
                    "Try smaller portions of rice or noodles."
                )

            # Simple protein recommendation
            if protein_percent < 10:
                recommendations.append(
                    "Try adding eggs, fish, tofu or beans."
                )

    # STEP 7: General healthy eating suggestion
    recommendations.append(
        "Try adding more vegetables to your meals."
    )

    # STEP 8: Disclaimer
    recommendations.append(
        "These are general food tips, not medical advice."
    )

    return recommendations


# ==========================================
# TEST THE RECOMMENDATIONS
# ==========================================

if __name__ == "__main__":

    # Demo user and date for testing
    user_id = 1
    selected_date = "2026-10-30"

    print("===== MAKANLENS DIET RECOMMENDATIONS =====")

    results = get_diet_recommendations(
        user_id, selected_date
    )

    for number, message in enumerate(results, 1):
        print(f"{number}. {message}")
