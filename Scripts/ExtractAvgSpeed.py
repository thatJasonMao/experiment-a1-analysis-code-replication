import os
import csv
from tqdm import tqdm

avg_speed_info = {}

info_line_index = 10

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

def analyze():
    target_folder = get_parent_folder_path() + os.sep + "GroupData"
    target_files = get_all_file_paths(target_folder)
    progress_bar = tqdm(total=len(target_files))
    for file in target_files:
        get_avg(file)
        progress_bar.update(1)
        progress_bar.set_description(f"计算速度均值")

def get_avg(path):
    global avg_speed_info
    frame_speed = []

    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) >= (info_line_index + 1):
                frame_speed.append(float(row[info_line_index]))

    total = sum(frame_speed)
    count = len(frame_speed)
    mean = total / count
    avg_speed_info[level_name] = mean
    # print("Avg Speed: " + str(mean))

def output():
    global avg_speed_info
    output_folder = get_parent_folder_path() + os.sep + "GroupData_Avg_Speed"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + "Result.csv"
    header = "Level,AvgSpeed"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in avg_speed_info.keys():
            header = key
            content = str(avg_speed_info[key])
            line = header + "," + content
            csvfile.write(line + "\n")

if __name__ == "__main__":
    analyze()
    output()
