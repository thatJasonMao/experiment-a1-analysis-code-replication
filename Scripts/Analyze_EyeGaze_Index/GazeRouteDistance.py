import math
import os
import csv
import numpy as np
from scipy.spatial.distance import cdist
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression

distance_dict = {}

def get_grand_grand_parent_folder():
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    grandparent_folder = os.path.dirname(parent_folder)
    return grandparent_folder

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def get_raw_data_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_All"
    return target_file_name

def get_data(path):
    raw_infos = []
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                sub_pos_x = float(row[1])
                sub_pos_y = float(row[2])
                sub_pos_z = float(row[3])
                sub_rot_y = float(row[5])

                gaze_pos_x = float(row[7])
                gaze_pos_y = float(row[8])
                gaze_pos_z = float(row[9])

                relative_pos = get_local_position(sub_pos_x,
                                                  sub_pos_z,
                                                  sub_pos_y,
                                                  sub_rot_y,
                                                  gaze_pos_x,
                                                  gaze_pos_z,
                                                  gaze_pos_y)
                raw_infos.append(relative_pos)
    return raw_infos

def execute():
    global distance_dict
    files = get_all_file_paths(get_raw_data_path())
    for file in files:
        level_name = os.path.basename(file)
        level_name = level_name.replace(".csv", "")
        track = get_data(file)
        print(f"Count: {files.index(file)}/{len(files)} 正在计算关卡：{level_name} 的注视轨迹长度 轨迹点数量：{len(track)}")
        distance = get_gaze_route_distance(track)
        distance_dict[level_name] = distance
        print(f"关卡：{level_name} 注视轨迹长度：{distance}")

    output_path = os.path.join(os.path.dirname(__file__), "GazeRouteDistance.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', '注视轨迹长度'])
        for level, value in distance_dict.items():
            writer.writerow([level, value])

def get_gaze_route_distance(points):
    total_distance = 0
    for i in range(len(points) - 1):
        x1, y1, z1 = points[i]
        x2, y2, z2 = points[i + 1]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        total_distance += distance

    return total_distance

def get_local_position(x_a, y_a, z_a, rotation_a, x_b, y_b, z_b):
    theta = np.radians(rotation_a)

    dx = x_b - x_a
    dy = y_b - y_a
    dz = z_b - z_a

    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],

        [np.sin(theta), np.cos(theta), 0],

        [0, 0, 1]

    ])

    translated_vector = np.array([dx, dy, dz])
    local_position = np.dot(rotation_matrix, translated_vector)

    return local_position

if __name__ == "__main__":
    execute()
