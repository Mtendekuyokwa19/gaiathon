import os, json
from detectron2.structures import BoxMode

def get_dumpsite_dicts(img_dir):
    dataset_dicts = []
    for idx, filename in enumerate(os.listdir(img_dir)):
        if not filename.endswith(".json"):
            continue
        json_path = os.path.join(img_dir, filename)
        with open(json_path) as f:
            data = json.load(f)

        record = {}
        image_path = os.path.join(img_dir, data["imagePath"])
        record["file_name"] = image_path
        record["image_id"] = idx
        record["height"] = 224  # change if your images are a different size
        record["width"] = 224

        objs = []
        for anno in data["shapes"]:
            px = [pt[0] for pt in anno["points"]]
            py = [pt[1] for pt in anno["points"]]
            poly = [(x, y) for x, y in zip(px, py)]
            poly_flat = [p for point in poly for p in point]

            obj = {
                "bbox": [min(px), min(py), max(px), max(py)],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": [poly_flat],
                "category_id": 0,  # only one class: dumpsite
            }
            objs.append(obj)

        record["annotations"] = objs
        dataset_dicts.append(record)
    return dataset_dicts
