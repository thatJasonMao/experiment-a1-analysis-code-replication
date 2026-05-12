import os
import csv
from tqdm import tqdm
import math

gaze_distance_info = {}

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
        get_gaze_distance(file)
        progress_bar.update(1)
        progress_bar.set_description(f"计算疏散全程的注视点距离")

def distance_between_two_points(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    z1 = pt1[2]

    x2 = pt2[0]
    y2 = pt2[1]
    z2 = pt2[2]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def get_gaze_distance(path):
    global gaze_distance_info
    frame_distance = []

    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        all_rows = list(reader)
        row_index = 1
        while row_index < len(all_rows):
            line = all_rows[row_index]
            x1 = float(line[1])
            y1 = float(line[2])
            z1 = float(line[3])
            p1 = [x1, y1, z1]
            x2 = float(line[22])
            y2 = float(line[23])
            z2 = float(line[24])
            p2 = [x2, y2, z2]
            cur_frame_distance = distance_between_two_points(p1, p2)
            frame_distance.append(cur_frame_distance)
            row_index = row_index + 1

    total = sum(frame_distance)
    avg = total / len(frame_distance)
    gaze_distance_info[level_name] = avg

def output():
    global gaze_distance_info
    output_folder = get_parent_folder_path() + os.sep + "GroupData_Gaze_Obj_Distance"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + "Result.csv"
    header = "Level,GazeObjDistance"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in gaze_distance_info.keys():
            header = key
            content = str(gaze_distance_info[key])
            line = header + "," + content
            csvfile.write(line + "\n")

if __name__ == "__main__":
    analyze()
    output()
