import os
from custom_data_loader import CustomDatasetLoader
from detectron2.config import get_cfg
from detectron2 import model_zoo
from custom_trainer import CustomTrainer

def train(cfg, output_dir, test_dataset_name):
    os.makedirs(output_dir, exist_ok=True)

    trainer = CustomTrainer(cfg)
    # Train the model
    trainer.resume_or_load(resume=False)
    trainer.train()

def main():
    # Registering the datasets
    custom_dataset_name = "aircraft_dataset"
    custom_dataset_dir = "datasets/aircraft_classification/train"
    custom_dataset_test_name = "aircraft_dataset_val"
    custom_dataset_test_dir = "datasets/aircraft_classification/test"
    data_loader = CustomDatasetLoader(custom_dataset_name, custom_dataset_dir)
    data_loader_test = CustomDatasetLoader(custom_dataset_test_name, custom_dataset_test_dir)
    data_loader.register_dataset()
    data_loader_test.register_dataset()

    # Train two different models with different hyperparameters, recommended by the official documentation
    cfg1 = get_cfg()
    cfg1.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg1.DATASETS.TRAIN = (custom_dataset_name,)
    #cfg1.DATASETS.TEST = (custom_dataset_test_name,)
    cfg1.DATALOADER.NUM_WORKERS = 2
    cfg1.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg1.SOLVER.IMS_PER_BATCH = 2
    cfg1.SOLVER.BASE_LR = 0.00025
    cfg1.SOLVER.MAX_ITER = 300
    cfg1.SOLVER.STEPS = []
    cfg1.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg1.MODEL.ROI_HEADS.NUM_CLASSES = 17
    cfg1.SOLVER.LOGGER_ITER = 10
    cfg1.OUTPUT_DIR = "output_dir1"

    train(cfg1, "output_dir1", custom_dataset_test_name)

    cfg2 = get_cfg()
    cfg2.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg2.DATASETS.TRAIN = (custom_dataset_name,)
    #cfg2.DATASETS.TEST = (custom_dataset_test_name,)
    cfg2.DATALOADER.NUM_WORKERS = 2
    cfg2.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg2.SOLVER.IMS_PER_BATCH = 4
    cfg2.SOLVER.BASE_LR = 0.0005
    cfg2.SOLVER.MAX_ITER = 400
    cfg2.SOLVER.STEPS = []
    cfg2.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg2.MODEL.ROI_HEADS.NUM_CLASSES = 17
    cfg2.SOLVER.LOGGER_ITER = 10
    cfg2.OUTPUT_DIR = "output_dir2"

    train(cfg2, "output_dir2", custom_dataset_test_name)

if __name__ == "__main__":
    main()