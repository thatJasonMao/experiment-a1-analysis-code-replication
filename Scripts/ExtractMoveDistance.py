import os
import csv
from tqdm import tqdm
import math

move_distance_info = {}

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
        get_distance(file)
        progress_bar.update(1)
        progress_bar.set_description(f"Computing total evacuation movement distance / 计算疏散全程总体运动距离")

def get_distance(path):
    global move_distance_info
    frame_distance = []

    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")

    last_pos = [0, 0, 0]
    current_pos = [0, 0, 0]

    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        all_rows = list(reader)
        row_index = 2
        first_pos_line = all_rows[1]
        first_pos_x = float(first_pos_line[1])
        first_pos_y = float(first_pos_line[2])
        first_pos_z = float(first_pos_line[3])
        last_pos = [first_pos_x, first_pos_y, first_pos_z]

        while row_index < len(all_rows):
            current_pos_line = all_rows[row_index]
            cur_pos_x = float(current_pos_line[1])
            cur_pos_y = float(current_pos_line[2])
            cur_pos_z = float(current_pos_line[3])
            current_pos = [cur_pos_x, cur_pos_y, cur_pos_z]

            frame_distance.append(distance_between_two_points(current_pos, last_pos))

            last_pos = current_pos
            row_index = row_index + 1

    level_total_distance = sum(frame_distance)
    move_distance_info[level_name] = level_total_distance

def distance_between_two_points(pt1, pt2):
    x1 = pt1[0]
    y1 = pt1[1]
    z1 = pt1[2]

    x2 = pt2[0]
    y2 = pt2[1]
    z2 = pt2[2]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

def output():
    global move_distance_info
    output_folder = get_parent_folder_path() + os.sep + "GroupData_Total_Move_Distance"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + "Result.csv"
    header = "Level,TotalMoveDistance"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in move_distance_info.keys():
            header = key
            content = str(move_distance_info[key])
            line = header + "," + content
            csvfile.write(line + "\n")

if __name__ == "__main__":
    analyze()
    output()
