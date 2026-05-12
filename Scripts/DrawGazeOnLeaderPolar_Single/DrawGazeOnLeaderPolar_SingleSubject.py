import os
import csv
import numpy as np
import matplotlib.pyplot as plt

single_subject_and_level_ref = "71f3213b10a309fd_B2"  # [隐私保护] 受试者姓名已替换为MD5哈希值

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

def get_polar_data_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_Leader_Full_Info_Polar"
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

                leader_pos_x = float(row[7])
                leader_pos_y = float(row[8])
                leader_pos_z = float(row[9])

                frame_data = [sub_pos_x, sub_pos_y, sub_pos_z, sub_rot_y, leader_pos_x, leader_pos_y, leader_pos_z]
                raw_infos.append(frame_data)
    return raw_infos

def draw_single_subject_single_level():
    if single_subject_and_level_ref != "":
        target_file = get_polar_data_path() + os.sep + single_subject_and_level_ref + ".csv"
        infos = get_data(target_file)

        local_pos = []
        for info in infos:
            new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
            local_pos.append(new_pos)

        x_coords = [point[0] for point in local_pos]
        y_coords = [point[1] for point in local_pos]

        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        width_inches = 2000 / 300
        height_inches = 2000 / 300
        plt.figure(figsize=(width_inches, height_inches))

        plt.scatter(x_coords, y_coords, color='blue', label='GazePoint')

        plt.title('领导者被注视时的相对位置 组别分类：' + single_subject_and_level_ref)
        plt.xlabel('X')
        plt.ylabel('Y')

        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(single_subject_and_level_ref + '.png', dpi=300)
        plt.close()

def get_local_position(x_a, y_a, rotation_a, x_b, y_b):
    rotation_rad = np.radians(rotation_a)

    translated_x = x_b - x_a
    translated_y = y_b - y_a

    rotation_matrix = np.array([
        [np.cos(rotation_rad), -np.sin(rotation_rad)],
        [np.sin(rotation_rad), np.cos(rotation_rad)]
    ])

    translated_vector = np.array([translated_x, translated_y])
    local_position = np.dot(rotation_matrix, translated_vector)

    return local_position

if __name__ == "__main__":
    draw_single_subject_single_level()
