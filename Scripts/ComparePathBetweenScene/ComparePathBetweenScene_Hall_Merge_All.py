import os
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.lines import Line2D

subject_traj_total_all_levels = []
subject_traj_security_all_levels = []
subject_traj_passenger_all_levels = []
subject_traj_robot_all_levels = []

leader_traj_total_all_levels = []
leader_traj_security_all_levels = []
leader_traj_passenger_all_levels = []
leader_traj_robot_all_levels = []

group_security = []
group_passenger = []
group_robot = []

total_level_list = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

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

def build_group_ref():
    global group_security
    global group_passenger
    global group_robot

    target_file_name = get_grand_grand_parent_folder() + os.sep + "Results" + os.sep + "Subject_Leader.csv"
    with open(target_file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                name = row[0]
                if "Passenger" in str(row[3]):
                    group_passenger.append(name)
                if "Security" in str(row[3]):
                    group_security.append(name)
                if "Robot" in str(row[3]):
                    group_robot.append(name)
    print("Passenger group total / Passenger组总计：" + str(len(group_passenger)))
    print("Security group total / Security组总计：" + str(len(group_security)))
    print("Robot group total / Robot组总计：" + str(len(group_robot)))

def build_traj_list():
    global group_security
    global group_passenger
    global group_robot

    global subject_traj_total_all_levels
    global subject_traj_security_all_levels
    global subject_traj_passenger_all_levels
    global subject_traj_robot_all_levels

    global leader_traj_total_all_levels
    global leader_traj_security_all_levels
    global leader_traj_passenger_all_levels
    global leader_traj_robot_all_levels

    group_data_path = get_grand_grand_parent_folder() + os.sep + "GroupData"
    files = get_all_file_paths(group_data_path)
    progress_bar = tqdm(total=len(files))
    for file in files:
        file_name = os.path.basename(file)
        subject_name = file_name.split("_")[0]
        for target_level in total_level_list:
            if target_level in file_name:
                new_subject_traj = []
                new_leader_traj = []

                with open(file, 'r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        sub_y_value = float(row[2])
                        if -12 < sub_y_value < -11.6:
                            sub_x = float(row[1])
                            sub_z = float(row[3])
                            new_subject_traj.append((sub_x, sub_z))
                        if "Leader" in str(row[34]):
                            leader_y_value = float(row[36])
                            if -12 < leader_y_value < -11.6:
                                leader_x = float(row[35])
                                leader_z = float(row[37])
                                new_leader_traj.append((leader_x, leader_z))

                if subject_name in group_security:
                    subject_traj_security_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_security_all_levels.append(new_leader_traj)
                    subject_traj_total_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_total_all_levels.append(new_leader_traj)

                if subject_name in group_passenger:
                    subject_traj_passenger_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_passenger_all_levels.append(new_leader_traj)
                    subject_traj_total_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_total_all_levels.append(new_leader_traj)

                if subject_name in group_robot:
                    subject_traj_robot_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_robot_all_levels.append(new_leader_traj)
                    subject_traj_total_all_levels.append(new_subject_traj)
                    if target_level != "A1":
                        leader_traj_total_all_levels.append(new_leader_traj)

        progress_bar.update(1)
        progress_bar.set_description(f"Extracting scene trajectory data / 提取场景轨迹数据")

def draw():
    global subject_traj_total_all_levels
    global subject_traj_security_all_levels
    global subject_traj_passenger_all_levels
    global subject_traj_robot_all_levels

    global leader_traj_total_all_levels
    global leader_traj_security_all_levels
    global leader_traj_passenger_all_levels
    global leader_traj_robot_all_levels

    draw_level(subject_traj_total_all_levels, leader_traj_total_all_levels, "Total")
    draw_level(subject_traj_security_all_levels, leader_traj_security_all_levels, "Security")
    draw_level(subject_traj_passenger_all_levels, leader_traj_passenger_all_levels, "Passenger")
    draw_level(subject_traj_robot_all_levels, leader_traj_robot_all_levels, "Robot")

def get_bg_path():
    root = get_grand_grand_parent_folder()
    plat_bg_pic = root + os.sep + "Shots" + os.sep + "Hall.png"
    return plat_bg_pic

def draw_level(subject_traj, leader_traj, name):
    pic_path = get_bg_path()

    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['font.sans-serif'] = ['Arial']

    width_inches = 1500 / 300
    height_inches = 2500 / 300
    plt.figure(figsize=(width_inches, height_inches))

    base_image = mpimg.imread(pic_path)
    flipped_base_image = np.flipud(base_image)

    base_height, base_width = flipped_base_image.shape[:2]
    x_offset = -base_width / 2
    y_offset = -base_height / 2

    scaled_subject_traj = []
    scaled_leader_traj = []

    for traj in subject_traj:
        x_coords = [point[0] * 12.85 for point in traj]
        y_coords = [point[1] * 12.85 for point in traj]
        scaled_subject_traj.append(list(zip(x_coords, y_coords)))

    if any(target_level != "A1" for target_level in total_level_list):
        for traj in leader_traj:
            x_coords = [point[0] * 12.85 for point in traj]
            y_coords = [point[1] * 12.85 for point in traj]
            scaled_leader_traj.append(list(zip(x_coords, y_coords)))

    negated_scaled_subject_traj = []
    for traj in scaled_subject_traj:
        new_traj = [(-x, -y) for x, y in traj]
        negated_scaled_subject_traj.append(new_traj)

    negated_scaled_leader_traj = []
    if any(target_level != "A1" for target_level in total_level_list):
        for traj in scaled_leader_traj:
            new_traj = [(-x, -y) for x, y in traj]
            negated_scaled_leader_traj.append(new_traj)

    y_offset_down = y_offset + 152

    plt.imshow(flipped_base_image, origin='upper',
               extent=[x_offset, x_offset + base_width, y_offset_down + base_height, y_offset_down])

    if name == "Total":
        global subject_traj_security_all_levels, subject_traj_passenger_all_levels, subject_traj_robot_all_levels
        group_colors = {
            "Security": "aqua",
            "Passenger": "deeppink",
            "Robot": "yellow"
        }

        for group_name, color in group_colors.items():
            traj_list = subject_traj_security_all_levels if group_name == "Security" \
                else subject_traj_passenger_all_levels if group_name == "Passenger" \
                else subject_traj_robot_all_levels

            for traj in traj_list:
                scaled_traj = [(x*12.85, z*12.85) for (x, z) in traj]
                negated_traj = [(-x, -z) for (x, z) in scaled_traj]
                x_coords = [p[0] for p in negated_traj]
                y_coords = [p[1] for p in negated_traj]
                plt.plot(x_coords, y_coords, marker='o', color=color,
                        markersize=0.06, linewidth=0.02)
    else:
        for traj in negated_scaled_subject_traj:
            x_coords = [point[0] for point in traj]
            y_coords = [point[1] for point in traj]
            plt.plot(x_coords, y_coords, marker='o', color='gold',
                    markersize=0.06, linewidth=0.02)

    show_leader = False
    if show_leader:
        if any(target_level != "A1" for target_level in total_level_list):
            for traj in negated_scaled_leader_traj:
                x_coords = [point[0] for point in traj]
                y_coords = [point[1] for point in traj]
                plt.plot(x_coords, y_coords, marker='o', color='tomato',
                        markersize=0.06, linewidth=0.02)

    plt.axis('equal')

    plt.gca().invert_yaxis()

    # plt.title(f"Trajectory All Levels Group:{name}", fontsize=18)

    plt.axis('off')

    legend_elements = [
        Line2D([0], [0], marker='o', color='aqua', label='Security',
               markersize=5, linestyle=''),
        Line2D([0], [0], marker='o', color='deeppink', label='Passenger',
               markersize=5, linestyle=''),
        Line2D([0], [0], marker='o', color='yellow', label='Robot',
               markersize=5, linestyle='')
    ]
    plt.legend(handles=legend_elements, loc='upper center', fontsize=13)

    plt.savefig("All_Levels_Hall_" + name + '.png', dpi=300, bbox_inches='tight', transparent=True)
    plt.close()

if __name__ == "__main__":
    build_group_ref()
    build_traj_list()
    draw()
