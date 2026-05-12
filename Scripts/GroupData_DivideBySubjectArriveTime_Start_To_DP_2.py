import os
import csv
from tqdm import tqdm

dp_3_4 = [(-31.71, -11.90, 30.60), (-30.71, -11.90, 30.60), (-31.71, -11.90, 37.60), (-30.71, -11.90, 37.60)]
dp_3_3 = [(30.71, -11.90, 30.60), (31.71, -11.90, 30.60), (30.71, -11.90, 37.60), (31.71, -11.90, 37.60)]
dp_3_2 = [(-31.71, -11.90, -61.33), (0-30.71, -11.90, -61.33), (-31.71, -11.90, -54.33), (-30.71, -11.90, -54.33)]
dp_3_1 = [(30.71, -11.90, -61.33), (31.71, -11.90, -61.33), (30.71, -11.90, -54.33), (31.71, -11.90, -54.33)]

dp_2_2 = [(3.53, -11.90, -45.06), (10.53, -11.90, -45.06), (3.53, -11.90, -44.06), (10.53, -11.90, -44.06)]
dp_2_1 = [(3.53, -11.90, 21.28), (10.53, -11.90, 21.28), (3.53, -11.90, 22.28), (10.53, -11.90, 22.28)]

def get_parent_folder_path():
    current_script_path = os.path.abspath(__file__)
    current_folder_path = os.path.dirname(current_script_path)
    parent_folder_path = os.path.dirname(current_folder_path)
    return parent_folder_path

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def divide_by_time():
    target_folder_path = get_parent_folder_path() + os.sep + "GroupData"
    files = get_all_file_paths(target_folder_path)
    # print(files)
    progress_bar = tqdm(total=len(files))
    for file in files:
        extract_start_to_dp2(file)
        progress_bar.update(1)
        progress_bar.set_description(f"提取从开始到DP2的实验数据")

def extract_start_to_dp2(path):
    level_key = path.split("\\")[len(path.split("\\")) - 1].replace(".csv", "")
    # print(level_key)
    has_found_dp_trigger = False
    dp_trigger_line_index = 0
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        line_counter = 0
        for row in reader:
            if len(row) > 1:
                line_counter = line_counter + 1
                subject_pos = (float(row[1]), float(row[2]), float(row[3]))
                if judge_subject_if_is_in_dp(subject_pos, dp_2_1, dp_2_2):
                    has_found_dp_trigger = True
                    dp_trigger_line_index = line_counter
                    break

    if has_found_dp_trigger:
        start_to_dp2_contents = read_csv_rows(path, dp_trigger_line_index)
        output_path = get_parent_folder_path() + os.sep + "GroupData_Start_To_DP2" + os.sep + level_key + ".csv"
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            for line in start_to_dp2_contents:
                str_line = ""
                for item in line:
                    str_line = str_line + str(item) + ","
                csvfile.write(str_line + "\n")

def read_csv_rows(file_path, dp_trigger_line_index):
    rows = []
    try:
        with open(file_path, 'r', newline='', errors='ignore') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i <= dp_trigger_line_index:
                    rows.append(row)
                else:
                    break
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"发生未知错误: {e}")

    return rows

def judge_subject_if_is_in_dp(subject_pos, p1, p2):
    x, _, z = subject_pos
    min_x_1 = min([point[0] for point in p1])
    max_x_1 = max([point[0] for point in p1])
    min_z_1 = min([point[2] for point in p1])
    max_z_1 = max([point[2] for point in p1])

    min_x_2 = min([point[0] for point in p2])
    max_x_2 = max([point[0] for point in p2])
    min_z_2 = min([point[2] for point in p2])
    max_z_2 = max([point[2] for point in p2])

    in_rect_1 = min_x_1 <= x <= max_x_1 and min_z_1 <= z <= max_z_1

    in_rect_2 = min_x_2 <= x <= max_x_2 and min_z_2 <= z <= max_z_2
    return in_rect_1 or in_rect_2

if __name__ == "__main__":
    divide_by_time()
