from PIL import Image
import os
import json

DATASET_DIR = "./dataset/resize/"  # or "./dumpsite_dataset/test" — repeat for both

TARGET_SIZE = (224, 224)

for file in os.listdir(DATASET_DIR):
    if file.endswith(".png") or file.endswith(".jpg"):
        img_path = os.path.join(DATASET_DIR, file)
        json_path = img_path.rsplit(".", 1)[0] + ".json"

        # Resize image
        with Image.open(img_path) as img:
            resized = img.resize(TARGET_SIZE)
            resized.save(img_path)

        # Update JSON annotation
        if os.path.exists(json_path):
            with open(json_path) as f:
                data = json.load(f)

            data["imageHeight"], data["imageWidth"] = TARGET_SIZE[1], TARGET_SIZE[0]

            with open(json_path, "w") as f:
                json.dump(data, f, indent=2)
