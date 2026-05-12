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
    test_mode = False
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

def draw_cloud():
    global gaze_leader_local_pos_security
    global gaze_leader_local_pos_passenger
    global gaze_leader_local_pos_robot

    import plotly.graph_objects as go

    GROUPS = [
        (gaze_leader_local_pos_security, 'Security Group', 'blue'),
        (gaze_leader_local_pos_passenger, 'Passenger Group', 'green'),
        (gaze_leader_local_pos_robot, 'Robot Group', 'red')
    ]

    for group_data, group_name, color in GROUPS:
        x_plot, y_plot, z_plot = [], [], []
        planar_distances = []

        for frame in group_data:
            dx = frame[3] - frame[0]
            dy_unity = frame[4] - frame[1]
            dz_unity = frame[5] - frame[2]

            yaw_rad = np.radians(frame[6])
            x_rot = dx * np.cos(yaw_rad) + dz_unity * np.sin(yaw_rad)
            z_rot = -dx * np.sin(yaw_rad) + dz_unity * np.cos(yaw_rad)

            x_plot.append(x_rot)
            y_plot.append(z_rot)
            z_plot.append(dy_unity)

            planar_distance = np.sqrt(x_rot**2 + z_rot**2)
            planar_distances.append(planar_distance)

        if planar_distances:
            max_distance = max(planar_distances)
            colors = [d / max_distance for d in planar_distances]

            # colors = planar_distances
        else:
            colors = []

        scatter = go.Scatter3d(
            x=x_plot,
            y=y_plot,
            z=z_plot,
            mode='markers',
            marker=dict(
                size=2,
                color=colors,

                colorscale='plasma',
                opacity=0.4,
                colorbar=dict(title='归一化距离(距离平面几何中心)', x=0.85),
                showscale=True
            ),
            name='注视点'
        )

        z = np.linspace(0, 1.7, 50)
        theta = np.linspace(0, 2 * np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_cyl = 0.2 * np.cos(theta_grid)
        y_cyl = 0.2 * np.sin(theta_grid)

        cylinder = go.Surface(
            x=x_cyl,
            y=y_cyl,
            z=z_grid,
            colorscale=[[0, '#888888'], [1, '#888888']],
            showscale=False,
            opacity=0.3,
            name='领导者模型'
        )

        layout = go.Layout(
            title=f'{group_name} - 眼动点分布',
            scene=dict(
                xaxis=dict(range=[-1, 1], title='X轴'),
                yaxis=dict(range=[-1, 1], title='Y轴'),
                zaxis=dict(range=[0, 2], title='Z轴'),
                aspectratio=dict(x=1, y=1, z=2)
            ),
            updatemenus=[dict(
                type="buttons",
                buttons=[
                    dict(label="俯视视角",
                         method="relayout",
                         args=["scene.camera", dict(eye=dict(x=0, y=0, z=2))]),
                    dict(label="前视视角",
                         method="relayout",
                         args=["scene.camera", dict(eye=dict(x=0.5, y=0.5, z=1))]),
                    dict(label="侧视视角",
                         method="relayout",
                         args=["scene.camera", dict(eye=dict(x=1, y=0, z=1))])],
                pad=dict(r=10, t=10),
                showactive=False,
            )]
        )

        fig = go.Figure(data=[scatter, cylinder], layout=layout)
        fig.write_html(f'GazeOnCapsule_{group_name.replace(" ", "")}_Interactive.html')

if __name__ == "__main__":
    build_group_ref()
    get_capsule_data()
    draw_cloud()
