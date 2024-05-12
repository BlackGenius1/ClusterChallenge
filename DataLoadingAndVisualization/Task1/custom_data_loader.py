import os
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.structures import BoxMode
from PIL import Image

class CustomDatasetLoader:
    def __init__(self, dataset_name, dataset_dir):
        self.dataset_name = dataset_name
        self.dataset_dir = dataset_dir

    def load_dataset(self):
        
        dataset_dicts = []
        # In my custom dataset the categories are represented by the folder names
        categories = os.listdir(self.dataset_dir)
        for category_id, category_name in enumerate(categories):
            category_dir = os.path.join(self.dataset_dir, category_name)
            # Go through the category folder and get all the images
            file_names = [f for f in os.listdir(category_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            for img_id, file_name in enumerate(file_names):
                record = {}
                # Image path
                file_path = os.path.join(category_dir, file_name)
                record["file_name"] = file_path
                # Image dimensions
                img = Image.open(file_path)
                record["width"], record["height"] = img.size
                # Annotations (bounding box coordinates)
                record["annotations"] = [
                    {
                    "bbox": [0, 0, record["width"], record["height"]],
                    "bbox_mode": BoxMode.XYXY_ABS,
                    "category_id": category_id,
                    }
                ]
                dataset_dicts.append(record)
        return dataset_dicts

    def register_dataset(self):
        DatasetCatalog.register(self.dataset_name, lambda: self.load_dataset())
        MetadataCatalog.get(self.dataset_name).set(thing_classes=list(os.listdir(self.dataset_dir)))
