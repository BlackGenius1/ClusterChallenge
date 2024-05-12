# Folder structure

 - Job files, screenshots and other files for the according tasks are       located in the folders named after the chapter. For some tasks I've added subfolders such as Task1 or Task2.
 -  Job names and other answers to tasks are stated below.
 - Code references are provided as links to the repositories below.

# Tasks

## Regular & Interactive Jobs

 1. Job name: example_26fd7a67
 2. Job name: vnc_6261f273
 3. Job name: vnc_473baf71

## Hot & Cold Network Storage

- Job name: vnc_66d30a26
- Code references: <br> script.py: https://github.com/BlackGenius1/ClusterChallenge/blob/main/script.py
- Note: I ran the job as vnc and connected to it via ssh. After that I uploaded my python script using scp and ran it via ssh. After my script executed successfully I downloaded the log files to my machine via scp.


## Containers & Virtual Environments

 1. Job name: waluschykjulian_8c044312 <br>
    Code References: https://github.com/serycjon/MFT (Used as ML repository) (See virtualEnvironment.yaml for the setup code)

 2. Job name: vnc_cc95502d <br>
    Note: The Dockerfile also installs git and clones the repository into the home directory in case it gets deleted from the hot storage somehow in the future. This guarantees, that the container will always have all the requirements installed.
    I am using master.garching.cluster.campar.in.tum.de:10443/camp/ubuntu_20.04-python_3.8-cuda_11.3-pytorch_1.11-gpu:latest as FROM, as it already provides python and torch.
    I pushed two versions to the docker registry. Version 1.5 is the latest. I also provided a screenshot.

## Data Loading & Visualization

 1. Job name: vnc_ed0eee71 <br>
 Notes: <br> I decided to use the detectron2 framework for this task, as it provides built-in datasets and well written documentation on how to use custom datasets and train them using the framework.
 I am using the built-in COCA dataset, and a Commercial Aircraft Dataset, which does not come in the COCO format. I created a .yaml which takes care of installing most of detectron2 and its dependecies and downloading the dataset.
 After that I created a custom dataloader to load my dataset, which also comes in a different file structure. To compare both datasets, my custom dataset and the built-in COCO dataset. I created the task_one_comparison_script.py,
 which uses the two different data loader and compares both datasets in terms of signal range. It also visualizes the data in both sets. Later I uploaded my dataset and my scripts using ssh and ran the comparison script to take the required screenshots. Since my data consists of thousands of images I could not visualize the entire dataset, that's why I decided to only visualize three images per dataset to compare them and see if the dataloader works correctly. In the folder structure you'll find the screenshots (Two screenshots for the visualization and one for the signal range output). To make sure that my dataset is in correct format I also visualized the annotations of random samples. Since there were no annotations (region data) in the dataset provided my custom data loader always applied the same coordinates for the visualizations. I didn't create an annotation json as it would've taken a lot of time and it was not explicitly required by the task. Of course, it would've been perfect to have well annotated images in the dataset to know exactly where the object is located, but I think it should also be okay to only have the object in the image correctly classified. You'll also find two screenshots of these visualization in the folder. I've also added the output in output.txt. Moreover you'll find my python scripts and below you'll find links to a repository, that also contains my scripts. <br>
 Code references: <br> 1. task_one_comparison_script.py: <br> 2. custom_data_loader.py:


 2. Job name: vnc_f2fbab77 <br>
 Notes: <br> For this task I used tensorboards SummaryWriter to log two training runs. To satisfy the requirements of this task I created my own writer which logs all the losses, metrics, network inputs and outputs.
 Detectron2 already comes with some built in logging framework, that's why I implemented my own logging functionality by creating a custom trainer-class with some extended logging functionality. I added my own function to log metrics and losses of the training process. After the training I copied all output files into the tensorboard folder. In the files you'll find screenshots of the tensorboard output to show the comparison of my two runs.
 I was trying to also include output images into the logging, which you can see in the code, but unfortunatly I was not able to access the modeled images. I was trying to find a working solution, but after 6 hours of desperatly searching for a solution I was really frustated and gave up. I was able to include some input images, which you can see in another screenshot.
 I was also not really sure if it makes sense to log input and output data if it consists only of images, rather than numeric data. The problem I encountered was, that I could not access any images from the self.data_loader, which is an attribute in the DefaultTrainer class, which I overwrote. The data was in a really strange format and I was not able to access it using
 strings or integers as indices. Finally I've attached all the log files, which my script generated during the two training runs.<br>
 Code references: <br> 1. training_logger.py: <br> 2. custom_trainer.py:
