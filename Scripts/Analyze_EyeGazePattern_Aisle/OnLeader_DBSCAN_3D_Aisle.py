import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.stats import gaussian_kde
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from mpl_toolkits.mplot3d import Axes3D

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

epsilon = 0.097

min_samples = 10

sub_folder_path = "Static_DBSCAN_OnLeader_3D"

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

def get_raw_data_path():
    target_file_name = get_grand_grand_parent_folder() + os.sep + "GroupData_Gaze_On_Leader_Full_Info_Polar"
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
                if -12 < sub_pos_y < -11.6 and sub_pos_x < -10.5:
                    raw_infos.append(frame_data)
                if -12 < sub_pos_y < -11.6 and sub_pos_x > 10.5:
                    raw_infos.append(frame_data)
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

def execute_dbscan(data_container, name):
    print(f"{name} data container length / {name}数据容器长度：{len(data_container)}")
    points = np.array(data_container)

    db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(points)
    labels = db.labels_

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise_percent = np.sum(labels == -1) / len(labels) * 100
    print(f"{name} clustering complete: {n_clusters} clusters found, noise {noise_percent:.1f}% / {name}聚类完成：找到{n_clusters}个簇，噪声点占比{noise_percent:.1f}%")

    plt.figure(figsize=(12, 12))
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.size'] = 24
    cmap = ListedColormap(['#999999'] + plt.cm.terrain(np.linspace(0, 1, n_clusters)).tolist())

    for cluster_id in range(-1, n_clusters):
        mask = (labels == cluster_id)
        if cluster_id == -1:
            plt.scatter(points[mask, 0], points[mask, 1], c='#999999',
                        s=10, alpha=0.3, label='Noise')
        else:
            plt.scatter(points[mask, 0], points[mask, 1],
                        c=[cmap(cluster_id + 1)],

                        s=10, alpha=0.6, label=f'Cluster {cluster_id}')

    plt.title(f'{name} DBSCAN Clustering', fontsize=45, y=1.05)
    plt.xlabel('X Position', fontsize=40)
    ax = plt.gca()
    ax.yaxis.set_label_coords(-0.12, 0.3)
    plt.ylabel('Y Position', rotation=270, va='top', ha='right', fontsize=40)

    plt.xticks(ticks=[-10, -5, 0, 5, 10], labels=['-10', '-5', '0', '5', '10'], fontsize=40)
    plt.yticks(ticks=[0, 5, 10, 15, 20], labels=['0', '5', '10', '15', '20'], fontsize=40)

    plt.grid(alpha=0.3)
    # plt.legend(markerscale=2, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.xlim(-10, 10)
    plt.ylim(0, 20)
    plt.gca().set_aspect('equal')

    output_path = f"{sub_folder_path}/{name}_DBSCAN.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=600)
    plt.close()

    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in labels else 0)

    m_labels = db.labels_
    m_mask = m_labels != -1
    silhouette_avg = silhouette_score(points[m_mask], labels[m_mask])

    valid_points = points[m_mask]
    if len(valid_points) > 1:

        xmin, xmax = -4, 4
        ymin, ymax = 0, 8
        xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([xx.ravel(), yy.ravel()])

        kernel = gaussian_kde(valid_points.T)
        f = np.reshape(kernel(positions).T, xx.shape)

        fig = plt.figure(figsize=(12, 12))
        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['font.size'] = 30
        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_surface(xx, yy, f, cmap='gist_earth',
                               rstride=1, cstride=1,
                               linewidth=0, antialiased=True)

        fig.colorbar(surf, shrink=0.75, aspect=12)

        ax.view_init(elev=30, azim=235)
        ax.set_title(f'{name} 3D KDE Visualization', x=0.62)

        ax.xaxis.labelpad = 15

        ax.yaxis.labelpad = 15

        ax.zaxis.labelpad = 25

        ax.zaxis.set_tick_params(pad=10)

        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ztext = ax.set_zlabel('Density')
        ax.set_zlim(0, 0.7)

        kde_path = f"{sub_folder_path}/{name}_KDE.png"
        plt.savefig(kde_path, dpi=600, bbox_inches='tight', bbox_extra_artists=[ztext])
        plt.close()
        print("3D KDE plot output complete / 三维KDE图输出完成")

    output_content = []
    output_content.append(f"=== {name} Group Cluster Report ===")
    output_content.append(f"Total clusters: {n_clusters}")
    output_content.append(f"Silhouette Score: {silhouette_avg:.3f}")
    output_content.append(f"Total points: {len(points)}")
    output_content.append(f"Noise points: {np.sum(labels == -1)} ({np.mean(labels == -1)*100:.1f}%)")
    output_content.append("------------------------------")

    for cluster_id in unique_labels:
        if cluster_id == -1:
            continue

        cluster_points = points[labels == cluster_id]
        angles = np.degrees(np.arctan2(cluster_points[:, 1], cluster_points[:, 0]))

        angles = (angles + 360) % 360

        distances = np.sqrt(cluster_points[:, 0] ** 2 + cluster_points[:, 1] ** 2)

        output_content.append(f"Cluster {cluster_id}:")
        output_content.append(f"  Point count: {len(cluster_points)}")
        output_content.append(f"  Angle range: {np.min(angles):.1f}° - {np.max(angles):.1f}°")
        output_content.append(f"  Distance range: {np.min(distances):.2f}m - {np.max(distances):.2f}m")
        output_content.append("------------------------------")

    file_name = f"{name}_cluster_info_eps{epsilon}_minsamp{min_samples}.txt"
    with open(os.path.join(sub_folder_path, file_name), 'w') as f:
        f.write('\n'.join(output_content))

if __name__ == "__main__":
    if not os.path.exists(sub_folder_path):
        os.mkdir(sub_folder_path)
    build_group_ref()
    build_data_ref()
    execute_dbscan(local_pos_security, "Security")
    execute_dbscan(local_pos_passenger, "Passenger")
    execute_dbscan(local_pos_robot, "Robot")
    execute_dbscan(local_pos_total, "Total")
