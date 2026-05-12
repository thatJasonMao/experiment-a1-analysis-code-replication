import os
import csv
from tqdm import tqdm
import math
from datetime import datetime

total_time_info = {}

def get_parent_folder_path():
    current_script_path = os.path.abspath(__file__)
    current_folder_path = os.path.dirname(current_script_path)
    parent_folder_path = os.path.dirname(current_folder_path)
    return parent_folder_path

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def text_timestamp_to_datetime(text_timestamp):
    parts = text_timestamp.split('_')
    year, month, day, hour, minute, second, millisecond = map(int, parts)
    return datetime(year, month, day, hour, minute, second, millisecond * 1000)

def analyze():
    target_folder = get_parent_folder_path() + os.sep + "GroupData"
    target_files = get_all_file_paths(target_folder)
    progress_bar = tqdm(total=len(target_files))
    for file in target_files:
        get_distance(file)
        progress_bar.update(1)
        progress_bar.set_description(f"Computing total evacuation travel time / 计算疏散全程旅行时间")

def get_distance(path):
    global total_time_info
    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        t1 = text_timestamp_to_datetime(all_rows[0][0])
        t2 = text_timestamp_to_datetime(all_rows[len(all_rows) - 1][0])
        delta_t = t2 - t1
        total_time_info[level_name] = str(delta_t.total_seconds())

def output():
    global total_time_info
    output_folder = get_parent_folder_path() + os.sep + "GroupData_Total_Travel_Time"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + "Result.csv"
    header = "Level,TotalTravelTime"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in total_time_info.keys():
            header = key
            content = str(total_time_info[key])
            line = header + "," + content
            csvfile.write(line + "\n")

if __name__ == "__main__":
    analyze()
    output()
