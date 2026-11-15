# ==========================================
# MAKANLENS MODULE 3
# STEP 11 - WELLNESS TRACKING
# ==========================================

# STEP 1: Import libraries
import sqlite3
from pathlib import Path

# STEP 2: Locate the existing database
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# ==========================================
# FUNCTION 1: CHECK WELLNESS TABLE COLUMNS
# ==========================================

def check_wellness_columns():

    # Connect to the database
    with sqlite3.connect(DB_PATH) as conn:

        # Retrieve the actual column names
        columns = conn.execute(
            "PRAGMA table_info(wellness_logs)"
        ).fetchall()

        # Return the column names
        return [column[1] for column in columns]


# ==========================================
# FUNCTION 2: VIEW WELLNESS RECORDS
# ==========================================

def get_wellness_history(user_id):

    # Connect to the database
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        # Retrieve wellness records for the user
        rows = conn.execute("""
            SELECT *
            FROM wellness_logs
            WHERE user_id = ?
        """, (user_id,)).fetchall()

        # Return records as dictionaries
        return [dict(row) for row in rows]


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("===== MAKANLENS WELLNESS TRACKER =====")

    # Show the columns in the database
    columns = check_wellness_columns()

    print("\nWellness table columns:")
    for column in columns:
        print("-", column)

    # Use existing demo user for testing
    user_id = 1

    # Read existing wellness records
    records = get_wellness_history(user_id)

    print("\n===== WELLNESS HISTORY =====")

    if records:
        for record in records:
            print(record)
    else:
        print("No wellness records yet.")


# ==========================================
# STEP 12 - SAVE OR UPDATE WELLNESS DATA
# ==========================================

# This function receives wellness information
# entered by the user through the interface.
#
# If the user already has a record for the date,
# the existing record will be updated.
#
# Otherwise, a new record will be created.

def save_wellness(user_id, log_date,
                  water_ml=None,
                  activity_minutes=None,
                  sleep_hours=None,
                  weight_kg=None):

    # STEP 1: Check that the input values are valid
    if water_ml is not None and water_ml < 0:
        raise ValueError("Water intake cannot be negative")

    if activity_minutes is not None and activity_minutes < 0:
        raise ValueError("Activity minutes cannot be negative")

    if sleep_hours is not None and not 0 <= sleep_hours <= 24:
        raise ValueError("Sleep hours must be between 0 and 24")

    if weight_kg is not None and weight_kg <= 0:
        raise ValueError("Weight must be greater than zero")

    # STEP 2: Connect to the SQLite database
    with sqlite3.connect(DB_PATH) as conn:

        # Enable foreign key checking
        conn.execute("PRAGMA foreign_keys = ON")

        # STEP 3: Check whether a record exists
        # for this user on the selected date
        existing = conn.execute("""
            SELECT log_id
            FROM wellness_logs
            WHERE user_id = ? AND log_date = ?
            ORDER BY log_id DESC
            LIMIT 1
        """, (user_id, log_date)).fetchone()

        # STEP 4: Update the existing record
        if existing:

            conn.execute("""
                UPDATE wellness_logs
                SET
                    water_ml = COALESCE(?, water_ml),
                    activity_minutes = COALESCE(?, activity_minutes),
                    sleep_hours = COALESCE(?, sleep_hours),
                    weight_kg = COALESCE(?, weight_kg)
                WHERE log_id = ?
            """, (
                water_ml,
                activity_minutes,
                sleep_hours,
                weight_kg,
                existing[0]
            ))

            return "Wellness record updated successfully!"

        # STEP 5: Insert a new record
        else:

            conn.execute("""
                INSERT INTO wellness_logs (
                    user_id,
                    log_date,
                    water_ml,
                    activity_minutes,
                    sleep_hours,
                    weight_kg
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                log_date,
                water_ml,
                activity_minutes,
                sleep_hours,
                weight_kg
            ))

            return "Wellness record saved successfully!"
