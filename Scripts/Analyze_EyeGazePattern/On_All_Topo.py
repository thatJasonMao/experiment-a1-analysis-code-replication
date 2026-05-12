import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

group_security = []
group_passenger = []
group_robot = []

infos_security = []
infos_passenger = []
infos_robot = []

local_pos_security = []
local_pos_passenger = []
local_pos_robot = []
local_pos_total = []

sub_folder_path = "Gaze_Topology"

file_tag = "OnAll"

global_top_percentage = 0.1

def calculate_elongation_index(boundary_points):
    if len(boundary_points) < 3:
        return None

    boundary_points = np.array(boundary_points)
    covariance_matrix = np.cov(boundary_points, rowvar=False)
    eigenvalues = np.linalg.eigvals(covariance_matrix)
    elongation_index = max(eigenvalues) / min(eigenvalues)
    return elongation_index

def calculate_concentration_index(sorted_intensity, total_intensity, top_percentage):
    threshold_index = int(top_percentage * len(sorted_intensity))
    top_intensity = np.sum(sorted_intensity[:threshold_index])
    concentration_index = top_intensity / total_intensity
    return concentration_index

def calculate_heatmap_center_and_percentage_boundary(data, top_percentage):
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]

    center_x = np.mean(x)
    center_y = np.mean(y)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[50, 50], range=[(-10, 10), (0, 20)])
    total_intensity = np.sum(heatmap)
    sorted_intensity = np.sort(heatmap.flatten())[::-1]

    threshold_index = int(top_percentage * len(sorted_intensity))
    threshold_value = sorted_intensity[threshold_index]

    high_intensity_points = np.argwhere(heatmap >= threshold_value)
    x_bin_centers = (xedges[:-1] + xedges[1:]) / 2
    y_bin_centers = (yedges[:-1] + yedges[1:]) / 2
    boundary_points = [(x_bin_centers[i], y_bin_centers[j]) for i, j in high_intensity_points]

    return (center_x, center_y), boundary_points, sorted_intensity, total_intensity

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

def get_raw_data_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_All"
    return target_file_name

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

def get_data(path):
    raw_infos = []
    try:
        with open(path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if len(row) > 1:
                    if "Leader" not in str(row[7]):
                        sub_pos_x = float(row[1])
                        sub_pos_y = float(row[2])
                        sub_pos_z = float(row[3])
                        sub_rot_y = float(row[5])

                        leader_pos_x = float(row[7])
                        leader_pos_y = float(row[8])
                        leader_pos_z = float(row[9])

                        frame_data = [sub_pos_x, sub_pos_y, sub_pos_z, sub_rot_y, leader_pos_x, leader_pos_y, leader_pos_z]
                        raw_infos.append(frame_data)
                    else:
                        print(f"略过一处不合规数据 {path}")
    except:
        print("文件读取错误：" + path)
    return raw_infos

def build_data_ref():
    global group_security
    global group_passenger
    global group_robot

    global infos_security
    global infos_passenger
    global infos_robot

    global local_pos_security
    global local_pos_passenger
    global local_pos_robot
    global local_pos_total

    files = get_all_file_paths(get_raw_data_path())

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        if subject_name in group_security:
            infos_security = infos_security + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        if subject_name in group_passenger:
            infos_passenger = infos_passenger + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        if subject_name in group_robot:
            infos_robot = infos_robot + get_data(file)

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

def plot_topology(data, title, ax, vmin, vmax):
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]

    x_range = (-10, 10)
    y_range = (0, 20)

    ax.set_xticks([-10, -5, 0, 5, 10])
    ax.set_yticks([0, 5, 10, 15, 20])
    ax.set_xticklabels(['-10', '-5', '0', '5', '10'])
    ax.set_yticklabels(['0', '5', '10', '15', '20'])

    bin_size = 0.2
    x_bins = int((x_range[1] - x_range[0]) / bin_size)
    y_bins = int((y_range[1] - y_range[0]) / bin_size)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[x_bins, y_bins], range=[x_range, y_range])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='gist_earth', vmin=0, vmax=vmax)

    center, boundary_points, sorted_intensity, total_intensity = calculate_heatmap_center_and_percentage_boundary(data, global_top_percentage)

    concentration_index = calculate_concentration_index(sorted_intensity, total_intensity, global_top_percentage)
    print(f"{title} - 热力质心: ({center[0]:.2f}, {center[1]:.2f}), 前10%集中度指数: {concentration_index:.4f}")

    elongation_index = calculate_elongation_index(boundary_points)

    ax.scatter(center[0], center[1], color='red', label='Heatmap Center')
    ax.text(
        -7.5, 19, f"Mass Center: ({center[0]:.3f}, {center[1]:.3f})",
        fontsize=11, color='black', bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="black")
    )
    ax.text(
        -9.2, 17.3, f"Top 10% Concentration Index: {concentration_index:.3f}",
        fontsize=11, color='black', bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="black")
    )
    ax.text(
        -6.2, 15.6, f"Elongation Index: {elongation_index:.3f}",
        fontsize=11, color='black', bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="black")
    )

    if boundary_points:
        boundary_points = np.array(boundary_points)
        if len(boundary_points) > 3:

            hull = ConvexHull(boundary_points)
            for simplex in hull.simplices:
                x_coords = boundary_points[simplex, 0]
                y_coords = boundary_points[simplex, 1]
                ax.plot(x_coords, y_coords, 'yellow', linewidth=1, label='Top 10% Boundary')

    ax.set_xlim(x_range)
    ax.set_ylim(y_range)

    ax.set_title(title, y=1.02)
    ax.set_xlabel('X Position',labelpad=1)
    ax.set_ylabel('Y Position', rotation=270, va='bottom', ha='center', labelpad=10)

    plt.colorbar(im, ax=ax, shrink=0.68, aspect=12)

if __name__ == "__main__":
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.sans-serif"] = ["Arial"]
    plt.rcParams["font.size"] = 13

    if not os.path.exists(sub_folder_path):
        os.mkdir(sub_folder_path)

    build_group_ref()
    build_data_ref()

    all_data = local_pos_security + local_pos_passenger + local_pos_robot
    all_data = np.array(all_data)
    vmin = np.min(all_data)
    vmax = np.max(all_data)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5), gridspec_kw={'wspace': 0.24})

    plot_topology(local_pos_security, 'Security Hotspot Topology', axes[1], 0, vmax)

    plot_topology(local_pos_passenger, 'Passenger Hotspot Topology', axes[0], 0, vmax)

    plot_topology(local_pos_robot, 'Robot Hotspot Topology', axes[2], 0, vmax)

    #plt.tight_layout()

    plt.savefig(f'{sub_folder_path}/{file_tag}_GazeField.png', dpi=600, bbox_inches='tight', transparent=True)
    plt.close()
