
# =====================================
# MAKANLENS MODULE 3
# STEP 12 - TEST WELLNESS UPDATE
# =====================================

from wellness_service import save_wellness, get_wellness_history

# Existing demo user
user_id = 1

# Update the existing demo record
result = save_wellness(
    user_id=1,
    log_date="2026-10-30",
    water_ml=1800,
    activity_minutes=40,
    sleep_hours=8.0,
    weight_kg=75
)

print(result)

# Retrieve wellness history from SQLite
history = get_wellness_history(user_id)

print("\n===== UPDATED WELLNESS HISTORY =====")

for record in history:
    print(record)
