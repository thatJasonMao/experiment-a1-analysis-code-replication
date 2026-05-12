import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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
    print("Passenger group total / Passenger组总计：" + str(len(group_passenger)))
    print("Security group total / Security组总计：" + str(len(group_security)))
    print("Robot group total / Robot组总计：" + str(len(group_robot)))

def get_polar_data_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_NPC_Full_Info"
    return target_file_name

def get_data(path):
    # print("Current Path:" + path)
    raw_infos = []
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                try:
                    sub_pos_x = float(row[1])
                    sub_pos_y = float(row[2])
                    sub_pos_z = float(row[3])
                    sub_rot_y = float(row[5])

                    npc_pos_x = float(row[7])
                    leader_pos_y = float(row[8])
                    leader_pos_z = float(row[9])

                    frame_data = [sub_pos_x, sub_pos_y, sub_pos_z, sub_rot_y, npc_pos_x, leader_pos_y, leader_pos_z]
                    raw_infos.append(frame_data)

                except:
                    print("Coordinate calculation error / 计算坐标出错 当前NPC注视文件路径 " + path + " 时间戳：" + str(row[0]))

    return raw_infos

def plot_scatter(data, title, ax, vmin, vmax):
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]

    x_range = (-10, 10)
    y_range = (0, 20)

    bin_size = 0.2
    x_bins = int((x_range[1] - x_range[0]) / bin_size)
    y_bins = int((y_range[1] - y_range[0]) / bin_size)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[x_bins, y_bins], range=[x_range, y_range])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    colors = plt.cm.plasma(np.linspace(0, 1, 256))
    colors[0] = [196/255, 223/255, 255/255, 1]

    custom_cmap = ListedColormap(colors)

    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap=custom_cmap, vmin=0, vmax=vmax)

    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.colorbar(im, ax=ax)

def draw_single_level_by_group():
    global group_security
    global group_passenger
    global group_robot

    infos_security = []
    infos_passenger = []
    infos_robot = []

    files = get_all_file_paths(get_polar_data_path())

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        level = level_name.split("_")[1]

        if subject_name in group_security and target_level in str(level):
            infos_security = infos_security + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        level = level_name.split("_")[1]
        if subject_name in group_passenger and target_level in str(level):
            infos_passenger = infos_passenger + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        level = level_name.split("_")[1]
        if subject_name in group_robot and target_level in str(level):
            infos_robot = infos_robot + get_data(file)

    local_pos_security = []
    local_pos_passenger = []
    local_pos_robot = []
    local_pos_total = []

    for info in infos_security:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_security.append(new_pos)
        local_pos_total.append(new_pos)

    for info in infos_passenger:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_passenger.append(new_pos)
        local_pos_total.append(new_pos)

    for info in infos_robot:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_robot.append(new_pos)
        local_pos_total.append(new_pos)

    all_data = local_pos_security + local_pos_passenger + local_pos_robot
    all_data = np.array(all_data)
    vmin = np.min(all_data)
    vmax = np.max(all_data)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    im1 = plot_scatter(local_pos_security, "Gaze On NPC  Level:" + target_level + ' Group:Security', axes[0], 0, vmax)

    im2 = plot_scatter(local_pos_passenger, "Gaze On NPC  Level:" + target_level + ' Group:Passenger', axes[1], 0, vmax)

    im3 = plot_scatter(local_pos_robot, "Gaze On NPC  Level:" + target_level + ' Group:Robot', axes[2], 0, vmax)

    plt.tight_layout()

    plt.savefig('GazeField.png', dpi=300)
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
    build_group_ref()
    draw_single_level_by_group()
