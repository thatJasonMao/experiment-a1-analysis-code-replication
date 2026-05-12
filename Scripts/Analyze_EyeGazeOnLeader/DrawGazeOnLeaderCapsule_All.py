import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

group_security = []
group_passenger = []
group_robot = []

gaze_leader_local_pos_security = []
gaze_leader_local_pos_passenger = []
gaze_leader_local_pos_robot = []

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

def get_local_gaze_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_Leader_Full_Info_Polar_Advanced"
    return target_file_name

def get_data(path):
    raw_infos = []
    raw_infos = []
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                leader_pos_x = float(row[7])
                leader_pos_y = float(row[8])
                leader_pos_z = float(row[9])

                hit_pos_x = float(row[10])
                hit_pos_y = float(row[11])
                hit_pos_z = float(row[12])

                leader_yaw = float(row[13])
                frame_data = [leader_pos_x, leader_pos_y, leader_pos_z, hit_pos_x, hit_pos_y, hit_pos_z, leader_yaw]
                raw_infos.append(frame_data)

    return raw_infos

def get_capsule_data():
    global group_security
    global group_passenger
    global group_robot

    global gaze_leader_local_pos_security
    global gaze_leader_local_pos_passenger
    global gaze_leader_local_pos_robot

    files = get_all_file_paths(get_local_gaze_path())
    test_mode = True
    if test_mode:
        test_frame_1 = [0, 0, 0, 0, 0, 0.8, 0]
        gaze_leader_local_pos_security.append(test_frame_1)
        gaze_leader_local_pos_passenger.append(test_frame_1)
        gaze_leader_local_pos_robot.append(test_frame_1)
        test_frame_2 = [0, 0, 0, 0.5, 0, 0, 0]
        gaze_leader_local_pos_security.append(test_frame_2)
        gaze_leader_local_pos_passenger.append(test_frame_2)
        gaze_leader_local_pos_robot.append(test_frame_2)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]

        if subject_name in group_security:
            gaze_leader_local_pos_security = gaze_leader_local_pos_security + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]

        if subject_name in group_passenger:
            gaze_leader_local_pos_passenger = gaze_leader_local_pos_passenger + get_data(file)

    for file in files:
        level_name = os.path.basename(file)
        subject_name = level_name.split("_")[0]

        if subject_name in group_robot:
            gaze_leader_local_pos_robot = gaze_leader_local_pos_robot + get_data(file)

    print(f"Passenger组注视数量总计{len(gaze_leader_local_pos_passenger)}")
    print(f"Security组注视数量总计{len(gaze_leader_local_pos_security)}")
    print(f"Robot组注视数量总计{len(gaze_leader_local_pos_robot)}")

def draw_capsule():
    global gaze_leader_local_pos_security
    global gaze_leader_local_pos_passenger
    global gaze_leader_local_pos_robot

    from mpl_toolkits.mplot3d import Axes3D

    VIEW_CONFIGS = [
        {'elev': 90, 'azim': 0, 'name': 'Top'},
        {'elev': 25, 'azim': -45, 'name': 'Front'},
        {'elev': 25, 'azim': 45, 'name': 'Side'}
    ]

    GROUPS = [
        (gaze_leader_local_pos_security, 'Security Group', 'blue'),
        (gaze_leader_local_pos_passenger, 'Passenger Group', 'green'),
        (gaze_leader_local_pos_robot, 'Robot Group', 'red')
    ]

    for group_data, group_name, color in GROUPS:
        fig = plt.figure(figsize=(24, 8))

        for view_idx, view_cfg in enumerate(VIEW_CONFIGS, 1):
            ax = fig.add_subplot(1, 3, view_idx, projection='3d')

            x_plot, y_plot, z_plot = [], [], []

            for frame in group_data:
                dx = frame[3] - frame[0]  # hitX - leaderX
                dy_unity = frame[4] - frame[1]

                dz_unity = frame[5] - frame[2]

                yaw_rad = np.radians(-frame[6])

                x_rot = dx * np.cos(yaw_rad) - dz_unity * np.sin(yaw_rad)
                z_rot = dx * np.sin(yaw_rad) + dz_unity * np.cos(yaw_rad)

                x_plot.append(x_rot)
                y_plot.append(z_rot)   # Unity Z -> matplotlib Y
                z_plot.append(dy_unity) # Unity Y -> matplotlib Z

            z = np.linspace(0, 1.7, 50)

            theta = np.linspace(0, 2 * np.pi, 50)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_cyl = 0.2 * np.cos(theta_grid)
            y_cyl = 0.2 * np.sin(theta_grid)
            ax.plot_surface(x_cyl, y_cyl, z_grid, alpha=0.3, color='#888888', edgecolor=None)
            z_bottom = np.zeros_like(theta_grid)
            ax.plot_surface(x_cyl, y_cyl, z_bottom, alpha=0.3, color='#888888', edgecolor=None)
            z_top = np.ones_like(theta_grid) * 1.7
            ax.plot_surface(x_cyl, y_cyl, z_top, alpha=0.3, color='#888888', edgecolor=None)

            ax.scatter(x_plot, y_plot, z_plot, c=color, s=0.5, alpha=0.4)

            ax.view_init(elev=view_cfg['elev'], azim=view_cfg['azim'])
            ax.set_xlim([-1, 1])
            ax.set_ylim([-1, 1])
            ax.set_zlim([0, 2])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f"{view_cfg['name']} View")

            x_ticks = [-1, -0.5, 0, 0.5, 1]
            ax.set_xticks(x_ticks)
            y_ticks = [-1, -0.5, 0, 0.5, 1]
            ax.set_yticks(y_ticks)
            z_ticks = [0, 0.5, 1, 1.5, 2]
            ax.set_zticks(z_ticks)

        plt.suptitle(group_name, y=0.9)
        plt.tight_layout()
        plt.savefig(f'GazeOnCapsule_{group_name.replace(" ", "")}.png', dpi=600)
        plt.close()

if __name__ == "__main__":
    build_group_ref()
    get_capsule_data()
    draw_capsule()
