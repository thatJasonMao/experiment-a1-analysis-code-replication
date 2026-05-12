import os
import csv
from tqdm import tqdm
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from tslearn.metrics import dtw

dtw_infos = {}

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

def read_and_calculate():
    target_file_path = get_parent_folder_path() + os.sep + "GroupData"
    target_files = get_all_file_paths(target_file_path)
    progress_bar = tqdm(total=len(target_files))
    for file in target_files:
        get_dtw(file)
        progress_bar.update(1)
        progress_bar.set_description(f"Computing subject-leader trajectory similarity / 计算受试者与领导者的轨迹相似性")

def get_dtw(path):
    global dtw_infos

    subject_traj = []
    leader_traj = []

    level_name = os.path.basename(path)
    if "A1" not in level_name:
        with open(path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if len(row) > 1:
                    if "Leader" in str(row[34]):
                        sub_pos_x = float(row[1])
                        sub_pos_y = float(row[2])
                        sub_pos_z = float(row[3])
                        sub_pos = [sub_pos_x, sub_pos_y, sub_pos_z]

                        leader_pos_x = float(row[35])
                        leader_pos_y = float(row[36])
                        leader_pos_z = float(row[37])
                        leader_pos = [leader_pos_x, leader_pos_y, leader_pos_z]

                        subject_traj.append(sub_pos)
                        leader_traj.append(leader_pos)

        dtw_distance = calculate_dtw_distance(subject_traj, leader_traj)
        dtw_infos[level_name] = dtw_distance

def calculate_dtw_distance(arg1, arg2):
    subject_trajectory = np.array(arg1)
    leader_trajectory = np.array(arg2)
    distance, _ = fastdtw(subject_trajectory, leader_trajectory, dist=euclidean)
    return distance

def out_put():
    global dtw_infos
    output_path = get_parent_folder_path() + os.sep + "Results" + os.sep + "TrajDTW.csv"
    header = "Level,DTW"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in dtw_infos.keys():
            line = key + "," + str(dtw_infos[key])
            csvfile.write(line + "\n")

if __name__ == "__main__":
    read_and_calculate()
    out_put()
