import json
from pathlib import Path

def read_module2_meal(json_path):
    path = Path(json_path)

    if not path.is_file():
        print("Meal JSON file not found.")
        print("Please export a meal from Module 2 first.")
        return None

    with open(path, "r", encoding="utf-8") as file:
        meal = json.load(file)

    required = [
        "food_name",
        "calories_kcal",
        "protein_g",
        "carbs_g",
        "fat_g"
    ]

    for key in required:
        if key not in meal:
            print("Missing information:", key)
            return None

    result = {
        "food_name": meal["food_name"],
        "calories": float(meal["calories_kcal"]),
        "protein": float(meal["protein_g"]),
        "carbs": float(meal["carbs_g"]),
        "fat": float(meal["fat_g"])
    }

    return result


if __name__ == "__main__":
    json_file = Path(__file__).parent / "makanlens_latest_meal.json"

    result = read_module2_meal(json_file)

    if result:
        print("=== MODULE 2 TO MODULE 3 ===")
        print("Food:", result["food_name"])
        print("Calories:", result["calories"], "kcal")
        print("Protein:", result["protein"], "g")
        print("Carbohydrates:", result["carbs"], "g")
        print("Fat:", result["fat"], "g")
        print("Nutrition data received successfully!")
