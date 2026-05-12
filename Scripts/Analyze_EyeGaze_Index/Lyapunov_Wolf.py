import os
import csv
import numpy as np
from scipy.spatial.distance import cdist
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression

lyapunov_dict_wolf = {}

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

def get_raw_data_path():
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

                gaze_pos_x = float(row[7])
                gaze_pos_y = float(row[8])
                gaze_pos_z = float(row[9])

                relative_pos = get_local_position(sub_pos_x,
                                                  sub_pos_z,
                                                  sub_pos_y,
                                                  sub_rot_y,
                                                  gaze_pos_x,
                                                  gaze_pos_z,
                                                  gaze_pos_y)
                raw_infos.append(relative_pos)
    return raw_infos

def execute():
    global lyapunov_dict_wolf
    files = get_all_file_paths(get_raw_data_path())
    for file in files:
        level_name = os.path.basename(file)
        level_name = level_name.replace(".csv", "")
        track = get_data(file)
        print(f"Count: {files.index(file)}/{len(files)} 正在计算关卡：{level_name} 的李雅普诺夫指数 轨迹点数量：{len(track)}")
        lyapunovs = get_lyapunov_wolf(track)
        lyapunov_dict_wolf[level_name] = lyapunovs
        print(f"关卡：{level_name} 李雅普诺夫指数：{lyapunovs}")

    output_path = os.path.join(os.path.dirname(__file__), "Lyapunov_Wolf.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'Lyapunov值'])
        for level, value in lyapunov_dict_wolf.items():
            writer.writerow([level, value])

def get_lyapunov_wolf(points, tau=1, P=10, max_iter=5, eps_scale=0.02):
    Y = np.asarray(points).T
    N = Y.shape[1]
    if Y.shape[0] == 1:

        m = 3

        Y = np.array([Y[0, i::tau] for i in range(m)])
        N = Y.shape[1]

    if P is None:
        fft_data = np.fft.rfft(Y[0])
        freqs = np.fft.rfftfreq(N)
        peaks, _ = find_peaks(np.abs(fft_data), prominence=0.5)
        P = int(1 / freqs[peaks[0]]) if peaks.size > 0 else 10

    eps_log = []
    for i in range(P, N - 1):
        ref_point = Y[:, i].reshape(1, -1)
        candidates = Y[:, :i - P].T if i > P else Y[:, :1].T
        if candidates.size == 0: continue

        distances = cdist(ref_point, candidates)[0]
        min_dist_initial = np.min(distances)
        current_eps = min_dist_initial * eps_scale
        nearest_idx, found = None, False

        for _ in range(max_iter):
            mask = distances <= current_eps
            valid_indices = np.where(mask)[0]
            if valid_indices.size > 0:
                nearest_idx = valid_indices[np.argmin(distances[valid_indices])]
                min_dist = distances[nearest_idx]
                found = True
                break
            current_eps *= 1.5

        if not found:

            nearest_idx = np.argmin(distances)
            min_dist = distances[nearest_idx]

        evolution = [max(min_dist, 1e-12)]

        max_track = min(50, N - i - 1)
        for j in range(1, max_track):
            pt_ref = Y[:, i + j]
            pt_near = Y[:, nearest_idx + j]
            distance = np.linalg.norm(pt_ref - pt_near)
            evolution.append(max(distance, 1e-12))

        valid_evolution = np.log(evolution)
        if not np.isinf(valid_evolution).any():
            eps_log.append(valid_evolution)

    if len(eps_log) == 0 or len(eps_log[0]) == 0:
        return np.nan

    try:
        max_len = max(len(seq) for seq in eps_log)
        y = np.zeros(max_len)
        count = np.zeros(max_len)
        for seq in eps_log:
            y[:len(seq)] += seq
            count[:len(seq)] += 1
        y = y / count

        t = np.arange(len(y))
        reg = LinearRegression().fit(t.reshape(-1, 1), y)
        return reg.coef_[0]
    except ValueError:
        print(f"回归失败")
        return np.nan

def get_local_position(x_a, y_a, z_a, rotation_a, x_b, y_b, z_b):
    theta = np.radians(rotation_a)

    dx = x_b - x_a
    dy = y_b - y_a
    dz = z_b - z_a

    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), 0],

        [np.sin(theta), np.cos(theta), 0],

        [0, 0, 1]

    ])

    translated_vector = np.array([dx, dy, dz])
    local_position = np.dot(rotation_matrix, translated_vector)

    return local_position

if __name__ == "__main__":
    execute()
