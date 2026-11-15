
from pathlib import Path
from module1_integration import predict_food, IMAGE_FOLDER


def prepare_module3_input(image_path):
    # Get food recognition result from Module 1
    prediction = predict_food(image_path)

    # Prepare data for Module 3
    # Nutrition values will come from Student 2
    result = {
        "class_index": prediction["class_index"],
        "food_name": prediction["food_name"],
        "confidence": prediction["confidence"],
        "calories": None,
        "protein": None,
        "carbs": None,
        "fat": None
    }

    return result


if __name__ == "__main__":
    print("=== MODULE 1 TO MODULE 3 ===")

    images = [
        p for p in IMAGE_FOLDER.rglob("*")
        if p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]

    if not images:
        print("No test images found.")
    else:
        data = prepare_module3_input(images[0])

        print("Testing:", images[0].name)
        print("Class index:", data["class_index"])
        print("Food name:", data["food_name"])
        print(
            "Confidence:",
            f"{data['confidence'] * 100:.2f}%"
        )

        print("Calories:", data["calories"])
        print("Protein:", data["protein"])
        print("Carbohydrates:", data["carbs"])
        print("Fat:", data["fat"])

        print("Integration data prepared successfully!")
