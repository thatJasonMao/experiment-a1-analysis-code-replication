import os
import csv
from tqdm import tqdm

infos = {}

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
        get_gaze_on_leader(file)
        progress_bar.update(1)
        progress_bar.set_description(f"Extracting gaze count / 提取注视次数")

def get_gaze_on_leader(path):
    global infos
    gaze_time_counter = 0
    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                if "Leader" in str(row[25]):
                    gaze_time_counter = gaze_time_counter + 1
    infos[level_name] = str(gaze_time_counter)

def output():
    global infos
    output_folder = get_parent_folder_path() + os.sep + "GroupData_Gaze_On_Leader_Time"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + "Result.csv"
    header = "Level,GazeOnLeaderTime"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in infos.keys():
            header = key
            content = str(infos[key])
            line = header + "," + content
            csvfile.write(line + "\n")

if __name__ == "__main__":
    analyze()
    output()
