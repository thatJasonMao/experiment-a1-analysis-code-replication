import os
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.stats import binned_statistic_2d
from matplotlib.colors import ListedColormap
from PIL import Image

subject_info_total = []
subject_info_security = []
subject_info_passenger = []
subject_info_robot = []

group_security = []
group_passenger = []
group_robot = []

total_level_list = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

merge_name = "Hall_Speed_Merge"

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

def build_traj_list(target_level):
    global group_security
    global group_passenger
    global group_robot

    global subject_info_total
    global subject_info_security
    global subject_info_passenger
    global subject_info_robot

    group_data_path = get_grand_grand_parent_folder() + os.sep + "GroupData"
    files = get_all_file_paths(group_data_path)
    progress_bar = tqdm(total=len(files))
    for file in files:
        file_name = os.path.basename(file)
        subject_name = file_name.split("_")[0]
        if target_level in file_name:
            new_subject_traj_with_plane_velocity = []

            with open(file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    sub_pos_y = float(row[2])
                    if -12 < sub_pos_y < -11.6:
                        subject_pos_x = float(row[1])
                        subject_pos_z = float(row[3])
                        subject_plane_velocity = float(row[10])
                        new_subject_traj_with_plane_velocity.append(
                            (subject_pos_x, subject_pos_z, subject_plane_velocity))

            if subject_name in group_security:
                subject_info_security.append(new_subject_traj_with_plane_velocity)
                subject_info_total.append(new_subject_traj_with_plane_velocity)

            if subject_name in group_passenger:
                subject_info_passenger.append(new_subject_traj_with_plane_velocity)
                subject_info_total.append(new_subject_traj_with_plane_velocity)

            if subject_name in group_robot:
                subject_info_robot.append(new_subject_traj_with_plane_velocity)
                subject_info_total.append(new_subject_traj_with_plane_velocity)

        progress_bar.update(1)
        progress_bar.set_description(f"Extracting scene trajectory data / 提取场景轨迹数据")

    print(f"Level {target_level} subject trajectory + velocity data count / 关卡 {target_level}  Subject轨迹+速度 数据数量数：" + str(len(subject_info_total)))

def draw():
    global subject_info_total
    global subject_info_security
    global subject_info_passenger
    global subject_info_robot

    draw_level(subject_info_total, "Total")
    # draw_level(subject_info_security, "Security")
    # draw_level(subject_info_passenger, "Passenger")
    # draw_level(subject_info_robot, "Robot")

def get_bg_path():
    root = get_grand_grand_parent_folder()
    plat_bg_pic = root + os.sep + "Shots" + os.sep + "Hall.png"
    return plat_bg_pic

def draw_level(subject_traj, name):
    pic_path = get_bg_path()

    scale_time = 12.85

    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['font.sans-serif'] = ['Arial']

    width_inches = 1500 / 300
    height_inches = 2500 / 300
    fig = plt.figure(figsize=(width_inches, height_inches))

    base_image = mpimg.imread(pic_path)
    flipped_base_image = np.flipud(base_image)

    base_height, base_width = flipped_base_image.shape[:2]
    x_offset = -base_width / 2
    y_offset = -base_height / 2

    scaled_subject_traj = []
    for traj in subject_traj:
        x_coords = [point[0] * scale_time for point in traj]
        y_coords = [point[1] * scale_time for point in traj]
        velocity = [point[2] for point in traj]
        scaled_subject_traj.append(list(zip(x_coords, y_coords, velocity)))

    negated_scaled_subject_traj = []
    for traj in scaled_subject_traj:
        new_traj = [(-x, -y, z) for x, y, z in traj]
        negated_scaled_subject_traj.append(new_traj)

    y_offset_down = y_offset + 152

    plt.imshow(flipped_base_image, origin='upper',
               extent=[x_offset, x_offset + base_width, y_offset_down + base_height, y_offset_down])

    new_flat_traj = [item for sublist in negated_scaled_subject_traj for item in sublist]
    final_traj_container = np.array(new_flat_traj)

    pos_x = final_traj_container[:, 0]
    pos_y = final_traj_container[:, 1]
    speed = final_traj_container[:, 2]

    min_x, max_x = np.min(pos_x), np.max(pos_x)
    min_y, max_y = np.min(pos_y), np.max(pos_y)

    bin_size = 0.5 * scale_time
    bins_x = int((max_x - min_x) / bin_size)
    bins_y = int((max_y - min_y) / bin_size)

    statistic, x_edge, y_edge, binnumber = binned_statistic_2d(
        pos_x, pos_y, speed, statistic='mean', bins=[bins_x, bins_y]
    )

    # reversed_custom_cmap = custom_cmap.reversed()

    im = plt.imshow(statistic.T, origin='lower', cmap='managua', extent=[x_edge[0], x_edge[-1], y_edge[0], y_edge[-1]], alpha=1)

    plt.axis('equal')

    # plt.gca().invert_yaxis()

    plt.axis('off')

    cbar = plt.colorbar(im,  shrink=0.75, label="Speed(m/s)")

    cbar.set_label("Speed(m/s)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

    plt.title(f'Velocity Distribution Scenario:{merge_name} Group:{name}', y=0.9, x=0.65, fontsize=15)

    plt.subplots_adjust(bottom=0)

    pic_name = f'{merge_name}_{name}.png'
    plt.savefig(pic_name, dpi=300, bbox_inches='tight', transparent=True)
    plt.close(fig)

    image = Image.open(f'{merge_name}_{name}.png')
    width, height = image.size
    crop_height = 240
    cropped_image = image.crop((0, 150, width, height - crop_height))
    cropped_image.save(f'{merge_name}_{name}.png')

if __name__ == "__main__":
    build_group_ref()
    for level in total_level_list:
        build_traj_list(level)
    draw()
