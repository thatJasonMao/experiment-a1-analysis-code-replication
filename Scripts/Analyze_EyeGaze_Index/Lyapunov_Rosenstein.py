import os
import csv
import numpy as np
from scipy.spatial.distance import cdist
from scipy.signal import find_peaks
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

lyapunov_dict_rosenstein = {}

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
    global lyapunov_dict_rosenstein
    files = get_all_file_paths(get_raw_data_path())
    progress_bar = tqdm(total=len(files), desc="Calculating Lyapunov Exponents")
    for file in files:
        level_name = os.path.basename(file)
        level_name = level_name.replace(".csv", "")
        track = get_data(file)
        print(f"Count: {files.index(file)}/{len(files)} 正在计算关卡：{level_name} 的李雅普诺夫指数 轨迹点数量：{len(track)}")
        lyapunovs = get_lyapunov_rosenstein(track)
        lyapunov_dict_rosenstein[level_name] = lyapunovs
        print(f"关卡：{level_name} 李雅普诺夫指数：{lyapunovs}")
        progress_bar.update(1)
    progress_bar.close()

    output_path = os.path.join(os.path.dirname(__file__), "Lyapunov_Rosenstein.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['level', 'Lyapunov值'])
        for level, value in lyapunov_dict_rosenstein.items():
            writer.writerow([level, value])

def get_lyapunov_rosenstein(points, tau=1, P=10):
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

    sum_log_d = []

    count = []

    for i in range(P, N - 1):
        ref_point = Y[:, i].reshape(1, -1)

        candidates = Y[:, :i - P].T if i > P else Y[:, :1].T
        if candidates.size == 0:
            continue

        distances = cdist(ref_point, candidates)[0]
        if len(distances) == 0:
            continue
        j = np.argmin(distances)

        min_dist = distances[j]

        j_origin = j

        max_k = min(N - i - 1, N - j_origin - 1)
        if max_k <= 0:
            continue

        for k in range(max_k + 1):
            pt_i = Y[:, i + k]
            pt_j = Y[:, j_origin + k]
            distance = np.linalg.norm(pt_i - pt_j)
            if distance < 1e-12:
                continue

            log_d = np.log(distance)
            while len(sum_log_d) <= k:
                sum_log_d.append(0.0)
                count.append(0)
            sum_log_d[k] += log_d
            count[k] += 1

    valid_k = []
    y_avg = []
    for k in range(len(sum_log_d)):
        if count[k] > 0:
            valid_k.append(k)
            y_avg.append(sum_log_d[k] / count[k])

    if not valid_k:
        return np.nan

    try:
        reg = LinearRegression().fit(np.array(valid_k).reshape(-1, 1), np.array(y_avg))
        return reg.coef_[0]
    except:
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
