
# MakanLens - Module 3
# User Profile and Calorie Calculation

def calculate_bmi(weight_kg, height_cm):
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Height and weight must be positive")

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


def calculate_calorie_target(
    age, gender, height_cm, weight_kg, activity_level
):
    if age <= 0 or height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Invalid profile information")

    # Calculate BMR
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender.lower() == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError("Unsupported gender for this formula")

    # Activity level
    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725
    }

    factor = activity_factors.get(activity_level.lower())

    if factor is None:
        raise ValueError("Invalid activity level")

    return round(bmr * factor)
