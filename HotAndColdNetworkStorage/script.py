import os
import random
import time
import string
import shutil
from zipfile import ZipFile

n1 = 10000
s1 = 100 * 1024
n2 = 100
s2 = 10 * 1024 * 1024
n3 = 1
s3 = 1024 * 1024 * 1024

hot_storage = "/mnt/scratch/"
cold_storage = "/mnt/workfiles/"

def generate_random_content(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def write_files(n, s):
    start_time = time.time()
    for i in range(n):
        with open(f"file_{i}.txt", "w") as file:
            file.write(generate_random_content(s))
    end_time = time.time()
    return end_time - start_time

def copy_files(source_folder, destination_folder):
    start_time = time.time()
    for file in os.listdir(source_folder):
        if file.startswith("file_"):
            shutil.copy(os.path.join(source_folder, file), os.path.join(destination_folder, file))
    end_time = time.time()
    return end_time - start_time

def copy_zip_file(name, source_folder, destination_folder):
    start_time = time.time()
    shutil.copy(os.path.join(source_folder, name), destination_folder)
    end_time = time.time()
    return end_time - start_time

def delete_files(directory):
    for file in os.listdir(directory):
        if file.startswith("file_"):
            os.remove(os.path.join(directory, file))

def archive_files(source_folder, zip_file):
    start_time = time.time()
    with ZipFile(zip_file, 'w') as zip_ref:
        for file in os.listdir(source_folder):
            if file.startswith("file_"):
                zip_ref.write(os.path.join(source_folder, file), file)
        zip_ref.close()
    end_time = time.time()
    return end_time - start_time

def extract_files(destination_folder, zip_file):
    start_time = time.time()
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    end_time = time.time()
    return end_time - start_time

def run_tasks(n, s):
    # Task 1: Create N files of size S
    write_time = write_files(n, s)
    # Task 2: Copy all files to scratch and back
    hot_copy_time = copy_files(".", os.path.join(hot_storage, f"{n}"))
    hot_copy_back_time = copy_files(".", os.path.join(hot_storage, f"{n}"))
    # Task 3: Copy all files to workfiles and back
    cold_copy_time = copy_files(".", os.path.join(cold_storage, f"{n}"))
    cold_copy_back_time = copy_files(os.path.join(cold_storage, f"{n}"), ".")
    # Task 4: Do Task 1 with fuse-zip
    zip_file = f"zip_file_{n}_{s}.zip"
    archive_time = archive_files(".", zip_file)
    copy_zip_file_time = copy_zip_file(zip_file, ".", os.path.join(hot_storage, "zip"))
    extract_time = extract_files(os.path.join(hot_storage, "zip"), zip_file)
    # delete everything
    delete_files(".")
    # Create logs
    with open(f"log{n}.log", "w") as file:
        file.write(f"Write time in container: {write_time:.2f} seconds\n")
        file.write(f"Hot Copy Duration: {hot_copy_time:.2f} seconds\n")
        file.write(f"Hot Copy Back Duration: {hot_copy_back_time:.2f} seconds\n")
        file.write(f"Cold Copy Duration: {cold_copy_time:.2f} seconds\n")
        file.write(f"Cold Copy Back Duration: {cold_copy_back_time:.2f} seconds\n")
        file.write(f"Archive Duration: {archive_time:.2f} seconds\n")
        file.write(f"Copy Zipfile Duration: {copy_zip_file_time:.2f} seconds\n")
        file.write(f"Extract Duration: {extract_time:.2f} seconds\n")


if __name__ == '__main__':
    run_tasks(n1, s1)
    run_tasks(n2, s2)
    run_tasks(n3, s3)
