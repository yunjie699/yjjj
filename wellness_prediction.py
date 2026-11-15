# ==========================================
# MAKANLENS - MODULE 3
# STEP 23: WELLNESS INSIGHTS & PREDICTION
# ==========================================

import sqlite3
from pathlib import Path
from datetime import date, timedelta

# STEP 1: Connect to existing group database
DB_PATH = Path(__file__).resolve().parent / "makanlens_group.db"


# STEP 2: Retrieve wellness records
def get_wellness_records(user_id, days=30):

    start_date = (date.today() - timedelta(days=days - 1)).isoformat()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT log_date, water_ml, sleep_hours,
                   activity_minutes, weight_kg
            FROM wellness_logs
            WHERE user_id = ?
              AND log_date >= ?
              AND log_date <= ?
            ORDER BY log_date ASC
        """, (user_id, start_date, date.today().isoformat())).fetchall()

    return [dict(row) for row in rows]


# STEP 3: Generate wellness insights
def get_wellness_insights(user_id):

    records = get_wellness_records(user_id)

    if not records:
        return [
            "No wellness records found in the last 30 days.",
            "Record water, sleep and activity to receive insights."
        ]

    insights = []

    # Only average values that were actually recorded
    water = [r["water_ml"] for r in records
             if r["water_ml"] is not None]

    sleep = [r["sleep_hours"] for r in records
             if r["sleep_hours"] is not None]

    activity = [r["activity_minutes"] for r in records
                if r["activity_minutes"] is not None]

    insights.append(
        f"Wellness records available: {len(records)} day(s)."
    )

    if water:
        avg_water = sum(water) / len(water)
        insights.append(
            f"Average logged water intake: {avg_water:.0f} ml."
        )
        if avg_water < 1500:
            insights.append(
                "REMINDER: Your average logged water intake "
                "is below the example 1500 ml tracking threshold."
            )

    if sleep:
        avg_sleep = sum(sleep) / len(sleep)
        insights.append(
            f"Average logged sleep: {avg_sleep:.1f} hours."
        )
        if avg_sleep < 7:
            insights.append(
                "REMINDER: Your average sleep is below "
                "7 hours. Consider improving sleep habits."
            )

    if activity:
        avg_activity = sum(activity) / len(activity)
        insights.append(
            f"Average logged activity: "
            f"{avg_activity:.0f} minutes per recorded day."
        )

    insights.append(
        "These insights use recorded data only "
        "and are not medical advice."
    )

    return insights


# STEP 4: Estimate weight trend
def predict_weight_trend(user_id):

    records = get_wellness_records(user_id)

    # Use only dates with recorded weight
    weights = [
        (date.fromisoformat(r["log_date"]), r["weight_kg"])
        for r in records
        if r["weight_kg"] is not None
    ]

    # Require at least 3 different dates
    if len(weights) < 3:
        return (
            "Insufficient weight history for prediction. "
            "Record weight on at least 3 different days."
        )

    first_date = weights[0][0]

    # Convert dates into elapsed days
    x = [(d - first_date).days for d, w in weights]
    y = [w for d, w in weights]

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    denominator = sum((v - mean_x) ** 2 for v in x)

    if denominator == 0:
        return "Insufficient date variation for prediction."

    # Simple linear regression
    slope = sum(
        (x[i] - mean_x) * (y[i] - mean_y)
        for i in range(n)
    ) / denominator

    # Estimate 7 days after latest record
    last_day = x[-1]
    predicted_weight = mean_y + slope * (
        last_day + 7 - mean_x
    )

    latest_weight = y[-1]

    if slope > 0.02:
        trend = "Increasing"
    elif slope < -0.02:
        trend = "Decreasing"
    else:
        trend = "Relatively stable"

    return {
        "latest_recorded_weight_kg": latest_weight,
        "trend": trend,
        "estimated_weight_after_7_days_kg": round(
            predicted_weight, 2
        ),
        "note": (
            "This is a simple mathematical trend estimate, "
            "not a reliable forecast or medical diagnosis."
        )
    }


# STEP 5: Test with existing database records
if __name__ == "__main__":

    user_id = 1

    print("===== MAKANLENS WELLNESS INSIGHTS =====")

    for number, insight in enumerate(
        get_wellness_insights(user_id), 1
    ):
        print(f"{number}. {insight}")

    print("\n===== WEIGHT TREND PREDICTION =====")
    print(predict_weight_trend(user_id))
