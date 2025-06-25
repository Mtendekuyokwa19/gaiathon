import cv2
import numpy as np
import os
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2 import model_zoo
from .dataset_utils import get_dumpsite_dicts

# Register dataset (only needs to be done once)
DatasetCatalog.register(
    "dumpsite_train", lambda: get_dumpsite_dicts("./dataset/train/")
)
MetadataCatalog.get("dumpsite_train").set(thing_classes=["dumpsite"])
metadata = MetadataCatalog.get("dumpsite_train")

# Load config
cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
cfg.MODEL.WEIGHTS = "output/model_final.pth"
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3
cfg.MODEL.DEVICE = "cpu"

predictor = DefaultPredictor(cfg)


def detect_dumpsites(image_path: str, output_dir: str = "predictions") -> str:
    """Detect dumpsites in an image and save annotated result. Returns path to saved image."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    outputs = predictor(image)
    instances = outputs["instances"].to("cpu")

    print(f"Total detections: {len(instances)}")

    # Filter by confidence threshold
    threshold = 0.3
    filtered_instances = instances[instances.scores > threshold]

    # Visualize
    visualizer = Visualizer(
        image[:, :, ::-1],
        metadata=metadata,
        scale=1.2,
        instance_mode=ColorMode.IMAGE_BW,
    )
    vis_output = visualizer.draw_instance_predictions(filtered_instances)

    # Build output path
    output_dir = output_dir = os.path.join("flaskr", "static")
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_dir, f"{base_filename}_detected.png")

    # Save image
    cv2.imwrite(output_path, vis_output.get_image()[:, :, ::-1])
    print(f"Saved visualization to: {output_path}")

    return f"{base_filename}_detected.png"
