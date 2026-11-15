# ============================================
# MAKANLENS MODULE 3
# STEP 16 - FEEDBACK HISTORY
# ============================================

import sqlite3
from pathlib import Path

# STEP 1: Locate existing group database
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# FUNCTION 1: Save feedback to SQLite
def save_feedback(user_id, message, rule_id=None):

    if not message or not message.strip():
        raise ValueError("Feedback message cannot be empty.")

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
            INSERT INTO feedback_messages
            (user_id, rule_id, message)
            VALUES (?, ?, ?)
        """, (user_id, rule_id, message))

    return "Feedback saved successfully!"


# FUNCTION 2: Retrieve feedback history
def get_feedback_history(user_id):

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT feedback_id, user_id,
                   created_at, rule_id, message
            FROM feedback_messages
            WHERE user_id = ?
            ORDER BY created_at DESC, feedback_id DESC
        """, (user_id,)).fetchall()

    return [dict(row) for row in rows]


# STEP 2: Test by reading existing feedback
# No new sample data is inserted automatically.
if __name__ == "__main__":

    user_id = 1

    print("===== FEEDBACK HISTORY =====")

    history = get_feedback_history(user_id)

    if history:
        for record in history:
            print("\nFeedback ID:", record["feedback_id"])
            print("Date:", record["created_at"])
            print("Rule:", record["rule_id"])
            print("Message:", record["message"])
    else:
        print("No feedback recorded yet.")
