import os
import json
import numpy as np
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.structures import BoxMode

# Adjust this to your actual dataset directory
DATASET_ROOT = "./dataset/"


def get_dumpsite_dicts(img_dir):
    dataset_dicts = []
    for filename in os.listdir(img_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(img_dir, filename)
            with open(json_path) as f:
                v = json.load(f)
            record = {
                "file_name": os.path.join(img_dir, v["imagePath"]),
                "image_id": filename[:-5],
                "height": v["imageHeight"],
                "width": v["imageWidth"],
                "annotations": [],
            }
            for shape in v["shapes"]:
                if shape["label"].lower() != "dumpsite":
                    continue
                px = [p[0] for p in shape["points"]]
                py = [p[1] for p in shape["points"]]
                poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
                poly = [coord for point in poly for coord in point]  # flatten

                obj = {
                    "bbox": [min(px), min(py), max(px), max(py)],
                    "bbox_mode": BoxMode.XYXY_ABS,
                    "segmentation": [poly],
                    "category_id": 0,
                }
                record["annotations"].append(obj)
            dataset_dicts.append(record)
    return dataset_dicts


# Register the dataset
DatasetCatalog.register(
    "dumpsite_train", lambda: get_dumpsite_dicts(os.path.join(DATASET_ROOT, "train"))
)
MetadataCatalog.get("dumpsite_train").set(thing_classes=["dumpsite"])

train_data = DatasetCatalog.get("dumpsite_train")
print(len(train_data))
