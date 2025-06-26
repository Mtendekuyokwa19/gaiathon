from detectron2.data import DatasetCatalog, MetadataCatalog
from dataset_utils import get_dumpsite_dicts
from detectron2.evaluation import COCOEvaluator
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
import os


class MyTrainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        os.makedirs(output_folder, exist_ok=True)
        return COCOEvaluator(dataset_name, cfg, False, output_folder)


# Fix the lambda closure issue - register datasets properly
def register_datasets():
    for d in ["train"]:
        dataset_name = f"dumpsite_{d}"
        dataset_path = f"./dataset/{d}/"

        # Register with a proper function, not lambda with closure issue
        DatasetCatalog.register(
            dataset_name, lambda path=dataset_path: get_dumpsite_dicts(path)
        )
        MetadataCatalog.get(dataset_name).set(thing_classes=["dumpsite"])


# Register datasets
register_datasets()

# Verify dataset registration
print("Registered datasets:", DatasetCatalog.list())
print("Training dataset length:", len(DatasetCatalog.get("dumpsite_train")))

# Configure the model
cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
)

# Dataset configuration
cfg.DATASETS.TRAIN = ("dumpsite_train",)
cfg.DATASETS.TEST = ()  # Empty tuple since we don't have test set

# Training configuration
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
)
cfg.SOLVER.IMS_PER_BATCH = 1
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = 1500  # Increased from 3 for better training
cfg.SOLVER.STEPS = []  # Empty steps for constant learning rate
cfg.SOLVER.GAMMA = 0.1

# Model configuration
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 64
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # dumpsite only

# Output configuration
cfg.OUTPUT_DIR = "./output"
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

# Evaluation configuration
cfg.TEST.EVAL_PERIOD = 50  # Evaluate every 50 iterations

print("Starting training...")
trainer = MyTrainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()

print("Training completed!")
print(f"Model saved to: {cfg.OUTPUT_DIR}")

# Since we don't have a test set, we can't run evaluation
# If you want to evaluate on the training set (not recommended for real evaluation):
# results = trainer.test(cfg, trainer.model)
# print("Evaluation results:", results)
