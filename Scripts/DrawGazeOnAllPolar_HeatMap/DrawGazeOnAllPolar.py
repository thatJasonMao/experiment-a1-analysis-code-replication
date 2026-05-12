import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.spatial import ConvexHull

group_security = []
group_passenger = []
group_robot = []

target_level_list = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

file_name = "Gaze Point Density"

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

def get_polar_data_path():
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

                leader_pos_x = float(row[7])
                leader_pos_y = float(row[8])
                leader_pos_z = float(row[9])

                frame_data = [sub_pos_x, sub_pos_y, sub_pos_z, sub_rot_y, leader_pos_x, leader_pos_y, leader_pos_z]
                raw_infos.append(frame_data)
    return raw_infos

def calculate_heatmap_center_and_percentage_boundary(data, top_percentage=0.1):
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

def calculate_concentration_index(sorted_intensity, total_intensity, top_percentage=0.1):
    threshold_index = int(top_percentage * len(sorted_intensity))
    top_intensity = np.sum(sorted_intensity[:threshold_index])
    concentration_index = top_intensity / total_intensity
    return concentration_index

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

    im = ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='gist_earth', vmin=0, vmax=vmax)

    center, boundary_points, sorted_intensity, total_intensity = calculate_heatmap_center_and_percentage_boundary(data, top_percentage=0.1)

    concentration_index = calculate_concentration_index(sorted_intensity, total_intensity, top_percentage=0.1)
    print(f"{title} - 热力质心: ({center[0]:.2f}, {center[1]:.2f}), 前10%集中度指数: {concentration_index:.4f}")

    ax.scatter(center[0], center[1], color='red', label='Heatmap Center')
    ax.text(
        -5.8, 18.5, f"Mass Center: ({center[0]:.3f}, {center[1]:.3f})",
        fontsize=12, color='black', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black")
    )
    ax.text(
        -7.5, 16.5, f"Top 10% Concentration Index: {concentration_index:.3f}",
        fontsize=12, color='black', bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black")
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

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    plt.colorbar(im, ax=ax, shrink=0.75)

def draw_by_group():
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

        if subject_name in group_security:
            infos_security = infos_security + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        level = level_name.split("_")[1]
        if subject_name in group_passenger:
            infos_passenger = infos_passenger + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]
        level = level_name.split("_")[1]
        if subject_name in group_robot:
            infos_robot = infos_robot + get_data(file)

    local_pos_security = []
    local_pos_passenger = []
    local_pos_robot = []

    for info in infos_security:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_security.append(new_pos)

    for info in infos_passenger:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_passenger.append(new_pos)

    for info in infos_robot:
        new_pos = get_local_position(info[0], info[2], info[3], info[4], info[6])
        local_pos_robot.append(new_pos)

    all_data = local_pos_security + local_pos_passenger + local_pos_robot
    all_data = np.array(all_data)
    vmin = np.min(all_data)
    vmax = np.max(all_data)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    plot_scatter(local_pos_security, file_name + ' (Group Security)', axes[0], 0, vmax)

    plot_scatter(local_pos_passenger, file_name + ' (Group Passenger)', axes[1], 0, vmax)

    plot_scatter(local_pos_robot, file_name + ' (Group Robot)', axes[2], 0, vmax)

    plt.tight_layout()

    plt.savefig('GazeField.png', dpi=600, bbox_inches='tight', transparent=True)
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
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.sans-serif"] = ["Arial"]
    build_group_ref()
    draw_by_group()
