import os
from detectron2.engine import DefaultTrainer
from detectron2.utils.visualizer import Visualizer
from tensorboardX import SummaryWriter
import torch

class CustomTrainer(DefaultTrainer):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.writer = SummaryWriter(log_dir=os.path.join(cfg.OUTPUT_DIR, "logs"))

    def train(self):
        super().train()
        self.log_metrics()

        # I tried to add input and output images to my logs
        for data in self.data_loader:
            for i in range(len(data)):
                image = data[i]["image"]
                image_out = image.to("cpu")
                # output = self.model(data[i])
                self.writer.add_image("input_image", image_out, global_step=self.iter)
                # self.writer.add_image("output_image", output[i]["image"], global_step=self.iter)

    def log_metrics(self):
        iteration = self.iter
        loss_dict = self.storage.latest()
        for key, value in loss_dict.items():
            if isinstance(value, torch.Tensor):
                self.writer.add_scalar(f"Loss/{key}", value.item(), iteration)
            else:
                print("Not a Tensor")
