import os
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

subject_traj_total = []
subject_traj_security = []
subject_traj_passenger = []
subject_traj_robot = []

leader_traj_total = []
leader_traj_security = []
leader_traj_passenger = []
leader_traj_robot = []

group_security = []
group_passenger = []
group_robot = []

target_level = "B5"

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
    print("Passenger组总计：" + str(len(group_passenger)))
    print("Security组总计：" + str(len(group_security)))
    print("Robot组总计：" + str(len(group_robot)))

def build_traj_list():
    global group_security
    global group_passenger
    global group_robot

    global subject_traj_total
    global subject_traj_security
    global subject_traj_passenger
    global subject_traj_robot

    global leader_traj_total
    global leader_traj_security
    global leader_traj_passenger
    global leader_traj_robot

    group_data_path = get_grand_grand_parent_folder() + os.sep + "GroupData"
    files = get_all_file_paths(group_data_path)
    progress_bar = tqdm(total=len(files))
    for file in files:
        file_name = os.path.basename(file)
        subject_name = file_name.split("_")[0]
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
                subject_traj_security.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_security.append(new_leader_traj)
                subject_traj_total.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_total.append(new_leader_traj)

            if subject_name in group_passenger:
                subject_traj_passenger.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_passenger.append(new_leader_traj)
                subject_traj_total.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_total.append(new_leader_traj)

            if subject_name in group_robot:
                subject_traj_robot.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_robot.append(new_leader_traj)
                subject_traj_total.append(new_subject_traj)
                if target_level != "A1":
                    leader_traj_total.append(new_leader_traj)

        progress_bar.update(1)
        progress_bar.set_description(f"提取场景轨迹数据")

def draw():
    global subject_traj_total
    global subject_traj_security
    global subject_traj_passenger
    global subject_traj_robot

    global leader_traj_total
    global leader_traj_security
    global leader_traj_passenger
    global leader_traj_robot

    draw_level(subject_traj_total, leader_traj_total, "Total")
    draw_level(subject_traj_security, leader_traj_security, "Security")
    draw_level(subject_traj_passenger, leader_traj_passenger, "Passenger")
    draw_level(subject_traj_robot, leader_traj_robot, "Robot")

def get_bg_path():
    root = get_grand_grand_parent_folder()
    plat_bg_pic = root + os.sep + "Shots" + os.sep + "Hall.png"
    return plat_bg_pic

def draw_level(subject_traj, leader_traj, name):
    pic_path = get_bg_path()

    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

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

    if target_level != "A1":
        for traj in leader_traj:
            x_coords = [point[0] * 12.85 for point in traj]
            y_coords = [point[1] * 12.85 for point in traj]
            scaled_leader_traj.append(list(zip(x_coords, y_coords)))

    negated_scaled_subject_traj = []
    for traj in scaled_subject_traj:
        new_traj = [(-x, -y) for x, y in traj]
        negated_scaled_subject_traj.append(new_traj)

    negated_scaled_leader_traj = []
    if target_level != "A1":
        for traj in scaled_leader_traj:
            new_traj = [(-x, -y) for x, y in traj]
            negated_scaled_leader_traj.append(new_traj)

    y_offset_down = y_offset + 152

    plt.imshow(flipped_base_image, origin='upper',
               extent=[x_offset, x_offset + base_width, y_offset_down + base_height, y_offset_down])

    for traj in negated_scaled_subject_traj:
        x_coords = [point[0] for point in traj]
        y_coords = [point[1] for point in traj]
        plt.plot(x_coords, y_coords, marker='o', color='gold', markersize=0.025, linewidth=0.01)

    if target_level != "A1":
        for traj in negated_scaled_leader_traj:
            x_coords = [point[0] for point in traj]
            y_coords = [point[1] for point in traj]
            plt.plot(x_coords, y_coords, marker='o', color='tomato', markersize=0.025, linewidth=0.01)

    plt.axis('equal')

    plt.gca().invert_yaxis()

    plt.title(f"Trajectory Level:{target_level} Group:{name}")

    plt.axis('off')

    plt.savefig(name + '.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    build_group_ref()
    build_traj_list()
    draw()
