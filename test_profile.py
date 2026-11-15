from profile_service import save_user_profile, get_user_profile

# Test using the existing demo account
# These are sample values, not real user data.

user_id = 1

result = save_user_profile(
    user_id=1,
    age=22,
    gender="Male",
    height_cm=170,
    weight_kg=75,
    activity_level="Moderately active"
)

print("===== PROFILE SAVED =====")
print("BMI:", result["bmi"])
print("Estimated maintenance calories:",
      result["estimated_maintenance_calories"], "kcal/day")

# Retrieve the profile from SQLite
profile = get_user_profile(user_id)

print("\n===== PROFILE FROM DATABASE =====")
if profile:
    for key, value in profile.items():
        print(key, ":", value)
else:
    print("Profile not found")
