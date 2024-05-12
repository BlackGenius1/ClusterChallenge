import numpy as np
import random
from PIL import Image
import matplotlib.pyplot as plt
from custom_data_loader import CustomDatasetLoader
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.utils.visualizer import Visualizer
import cv2

def calculate_signal_range(dataset_dicts):
    signal_values = []
    for d in dataset_dicts:
        img = Image.open(d["file_name"])
        signal_values.append(np.array(img).mean()) # Calculating mean pixel value

    # Convert the list to numpy array for calculations
    signal_values = np.array(signal_values)
    # Calculate min, max, and mean
    signal_min = np.min(signal_values)
    signal_max = np.max(signal_values)
    signal_mean = np.mean(signal_values)
    return signal_min, signal_max, signal_mean

def visualize_data(dataset_dicts, dataset_name, num_images=3):
    # As it is difficult to visualize all data, I specified num_images, which sets the amount of pictures to visualize
    plt.figure(figsize=(12, 6))
    for i in range(num_images):
        d = random.choice(dataset_dicts)
        img = Image.open(d["file_name"])
        plt.subplot(1, num_images, i + 1)
        plt.imshow(img)
        plt.title(f"Image {i+1}")
        plt.axis('off')
    plt.show()

    # To verify the dataset is in correct format I also visualized the annotations (categories) of random samples
    plt.figure(figsize=(12, 6))
    for i in range(num_images):
        d = random.choice(dataset_dicts)
        img = cv2.imread(d["file_name"])
        plt.subplot(1, num_images, i + 1)
        visualizer = Visualizer(img[:, :, ::-1], metadata=MetadataCatalog.get(dataset_name), scale=0.5)
        out = visualizer.draw_dataset_dict(d)
        plt.imshow(out.get_image()[:, :, ::-1])
        plt.title(f"Image {i+1}")
        plt.axis('off')        
    plt.show()


def main():
    # Load custom dataset and built-in Detectron2 dataset
    custom_dataset_name = "aircraft_dataset"
    custom_dataset_dir = "datasets/aircraft_classification/train"
    data_loader = CustomDatasetLoader(custom_dataset_name, custom_dataset_dir)
    data_loader.register_dataset()
    custom_dataset_dicts = DatasetCatalog.get(custom_dataset_name)

    built_in_dataset_name = "coco_2017_train"
    built_in_dataset_dicts = DatasetCatalog.get(built_in_dataset_name)

    # Calculate signal range for both datasets
    custom_min, custom_max, custom_mean = calculate_signal_range(custom_dataset_dicts)
    built_in_min, built_in_max, built_in_mean = calculate_signal_range(built_in_dataset_dicts)

    # Print the results
    print("Custom Dataset Signal Range:")
    print("Min:", custom_min)
    print("Max:", custom_max)
    print("Mean:", custom_mean)
    print("\nBuilt-in Detectron2 Dataset Signal Range:")
    print("Min:", built_in_min)
    print("Max:", built_in_max)
    print("Mean:", built_in_mean)

    # Visualize the data from both datasets to compare them
    print("Visualizing custom dataset images:")
    visualize_data(custom_dataset_dicts, custom_dataset_name)
    print("Visualizing built-in dataset images:")
    visualize_data(built_in_dataset_dicts, built_in_dataset_name)

if __name__ == "__main__":
    main()