
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array

# Location of Student 1's Module 1
MODULE1_FOLDER = (
    Path.home()
    / "Downloads"
    / "MAKANLENS-MODULE1-main"
    / "MAKANLENS-MODULE1-main"
)

MODEL_PATH = (
    MODULE1_FOLDER
    / "Model"
    / "Model"
    / "efficientnetb0_model.keras"
)

CLASS_NAMES_PATH = MODULE1_FOLDER / "class_names.txt"
IMAGE_FOLDER = MODULE1_FOLDER / "test_images"


def predict_food(image_path):
    # Check files
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not CLASS_NAMES_PATH.is_file():
        raise FileNotFoundError(
            f"Class names file not found: {CLASS_NAMES_PATH}"
        )

    # Read food class names
    with open(CLASS_NAMES_PATH, "r", encoding="utf-8-sig") as file:
        class_names = [
            line.strip()
            for line in file
            if line.strip()
        ]

    if not class_names:
        raise ValueError("class_names.txt is empty.")

    # Load Student 1's AI model
    model = tf.keras.models.load_model(
        str(MODEL_PATH),
        compile=False
    )

    # Prepare image
    image = load_img(
        str(image_path),
        target_size=(224, 224),
        color_mode="rgb"
    )

    image_array = img_to_array(image)
    input_array = np.expand_dims(image_array, axis=0)

    # Predict food
    predictions = model.predict(
        input_array,
        verbose=0
    )[0]

    # Check number of classes
    if len(class_names) != len(predictions):
        raise ValueError(
            f"Model has {len(predictions)} outputs, "
            f"but class_names.txt has {len(class_names)} labels."
        )

    predicted_index = int(np.argmax(predictions))
    predicted_food = class_names[predicted_index]
    confidence = float(predictions[predicted_index])

    return {
        "class_index": predicted_index,
        "food_name": predicted_food,
        "confidence": confidence
    }


if __name__ == "__main__":
    print("=== MAKANLENS MODULE 1 TEST ===")

    images = [
        p for p in IMAGE_FOLDER.rglob("*")
        if p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]

    if not images:
        print("No test images found.")
    else:
        result = predict_food(images[0])

        print("Testing:", images[0].name)
        print("Class index:", result["class_index"])
        print("Food name:", result["food_name"])
        print(
            "Confidence:",
            f"{result['confidence'] * 100:.2f}%"
        )

        print("Module 1 test completed!")
