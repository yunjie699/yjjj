# ============================================
# MAKANLENS MODULE 3
# STEP 17 - FEEDBACK INTEGRATION TEST
# ============================================

from feedback_service import generate_feedback
from feedback_history import (
    save_feedback,
    get_feedback_history
)

# STEP 1: Use the existing demo user
user_id = 1

# STEP 2: Select a date with recorded data
selected_date = "2026-10-30"

# STEP 3: Generate feedback from existing data
feedback = generate_feedback(user_id, selected_date)

print("===== GENERATED FEEDBACK =====")

# STEP 4: Save each generated message
for number, message in enumerate(feedback, start=1):
    print(f"{number}. {message}")

    result = save_feedback(
        user_id=user_id,
        message=message,
        rule_id="PERSONALISED_FEEDBACK"
    )

    print(result)

# STEP 5: Retrieve saved feedback
print("\n===== SAVED FEEDBACK HISTORY =====")

history = get_feedback_history(user_id)

for record in history:
    print(
        f"ID: {record['feedback_id']} | "
        f"Message: {record['message']}"
    )
