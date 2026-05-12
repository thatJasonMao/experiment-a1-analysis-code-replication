import datetime
import os
import csv
from datetime import datetime
from tqdm import tqdm
import glob
from collections import defaultdict

level_names = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']

process_start_key_log = "Unfreeze Subject Agent Move"
process_end_key_log = "Subject Agent Has Arrive"

standard_time_stamps = []

def build_time_reference():
    for name in level_names:
        build_level_data(name)

def build_level_data(level_name):
    global standard_time_stamps
    standard_time_stamps.clear()
    target_folder_path = get_current_folder_path() + os.sep + level_name
    files = get_all_file_paths(target_folder_path)
    if len(files) == 4:
        log_file_path = ""
        log_file_key_word = level_name + "_Log_Info"
        for file in files:
            if log_file_key_word in file:
                log_file_path = file
        log_contents = read_log_content(log_file_path)
        start_time_stamp = get_start_timestamp(log_contents)
        end_time_stamp = get_end_timestamp(log_contents)
        # print("Start:" + start_time_stamp + " End:" + end_time_stamp)
        print("\n\nCurrent Level:" + level_name)
        subject_dict = build_subject_content(start_time_stamp, end_time_stamp, level_name)
        gaze_dict = build_gaze_content(level_name)
        npc_dict = build_npc_content(level_name)

        subject_header = "TimeStamp,PosX,PosY,PosZ,VeloX,VeloY,VeloZ,RotX,RotY,RotZ,AbsVelo,AccX,AccY,AccZ,StickX,StickY,"
        eye_gaze_header = "HeadRotX,HeadRotY,HeadRotZ,GazeDirX,GazeDirY,GazeDirZ,Hit1_X,Hit1_Y,Hit1_Z,Hit1_Name,Hit2_X,Hit2_Y,Hit2_Z,Hit2_Name,Hit3_X,Hit3_Y,Hit3_Z,Hit3_Name,"
        npc_item_header = "Name,PosX,PosY,PosZ,VeloX,VeloY,VeloZ,RotX,RotY,RotZ,AbsVelo,"

        total_header = subject_header + eye_gaze_header + npc_item_header * 65
        out_put_path = get_proj_folder_name() + os.sep + "GroupData" + os.sep + get_current_subject_name() + "_" + level_name + ".csv"
        # print(out_put_path)
        with open(out_put_path, mode='w', encoding='utf-8', newline='') as file:
            file.write(total_header + "\n")
            for key in standard_time_stamps:
                line_time_stamp = dt_to_str(key)
                line_content = subject_dict[key] + gaze_dict[key] + npc_dict[key]
                line = line_time_stamp + "," + line_content
                file.write(line + "\n")

def build_subject_content(start_time, end_time, level):
    inner_dict = {}
    subject_file_keyword = level + "_Subject_Simulation_Info"
    subject_file_path = ""
    target_file_path = get_current_folder_path() + os.sep + level
    files = get_all_file_paths(target_file_path)
    for file in files:
        if subject_file_keyword in file:
            subject_file_path = file
    # print(subject_file_path)

    full_file_contents = read_csv_all_lines(subject_file_path)
    # print("Subject File Content Count:" + str(len(full_file_contents)))

    progress_bar = tqdm(total=len(full_file_contents))
    global standard_time_stamps
    line_index = 0
    while line_index < len(full_file_contents):
        progress_bar.update(1)
        progress_bar.set_description(f"Extracting subject data / 提取受试者数据")

        line = full_file_contents[line_index]
        str_stamp = line[0]
        str_line_content = ','.join(line)
        # print(str_line_content)
        current_time = text_timestamp_to_datetime(str_stamp)
        if current_time > text_timestamp_to_datetime(start_time):
            if current_time < text_timestamp_to_datetime(end_time):
                standard_time_stamps.append(current_time)

                header = str_stamp + ","
                line_content = str_line_content.replace(header, "")
                # print(line_content)
                inner_dict[current_time] = line_content
        line_index = line_index + 1
    progress_bar.close()
    return inner_dict

def build_gaze_content(level):
    inner_dict = {}
    gaze_file_key_word = level + "_EyeGaze_Simulation"
    gaze_file_path = ""
    target_file_path = get_current_folder_path() + os.sep + level
    files = get_all_file_paths(target_file_path)
    for file in files:
        if gaze_file_key_word in file:
            gaze_file_path = file

    full_file_contents = read_csv_all_lines(gaze_file_path)
    # print("Subject File Content Count:" + str(len(full_file_contents)))

    progress_bar = tqdm(total=len(full_file_contents))
    global standard_time_stamps
    line_index = 0
    while line_index < len(full_file_contents):
        progress_bar.update(1)
        progress_bar.set_description(f"Extracting eye-tracking data / 提取眼动数据")
        line = full_file_contents[line_index]
        str_stamp = line[0]
        str_line_content = ','.join(line)
        # print(str_line_content)
        current_time = text_timestamp_to_datetime(str_stamp)
        if current_time in standard_time_stamps:
            header = str_stamp + ","
            line_content = str_line_content.replace(header, "")
            # print(line_content)
            inner_dict[current_time] = line_content
        line_index = line_index + 1

    progress_bar.close()
    return inner_dict

def build_npc_content(level):
    npc_file_key_word = f"{level}_NPC_Simulation_Info"
    target_dir = os.path.join(get_current_folder_path(), level)

    npc_files = glob.glob(os.path.join(target_dir, f"*{npc_file_key_word}*"))
    if not npc_files:
        raise FileNotFoundError(f"NPC文件未找到: 包含关键词{npc_file_key_word}")
    npc_file_path = npc_files[0]

    full_file_contents = read_csv_all_lines(npc_file_path)

    time_stamp_map = defaultdict(list)
    for line in full_file_contents:
        str_stamp = line[0]
        line_time = text_timestamp_to_datetime(str_stamp)
        processed_line = ','.join(line[1:])
        time_stamp_map[line_time].append(processed_line)
        # print(processed_line)

    global standard_time_stamps
    inner_dict = {}

    with tqdm(standard_time_stamps, desc="提取NPC数据") as progress_bar:
        for ts in progress_bar:
            lines = time_stamp_map.get(ts, [])
            inner_dict[ts] = ''.join(lines)

            # print(str(inner_dict[ts]))
            # quit()

    return inner_dict

def read_log_content(log_file_path):
    contents = []
    with open(log_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 1:
                contents.append(row[0])
    return contents

def read_csv_all_lines(path):
    all_rows = []
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            all_rows.append(row)
    return all_rows

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def get_current_folder_path():
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    return current_folder

def get_start_timestamp(logs):
    global process_start_key_log
    timestamp = "Null"
    for log in logs:
        if process_start_key_log in str(log):
            timestamp = log.split(" [Info]", maxsplit=1)[0]
            timestamp = timestamp.replace("[", "")
            timestamp = timestamp.replace("]", "")
    # print("Start Time:" + timestamp)
    return timestamp

def text_timestamp_to_datetime(text_timestamp):
    # print("Raw Time:" + text_timestamp)
    parts = text_timestamp.split('_')
    year, month, day, hour, minute, second, millisecond = map(int, parts)
    return datetime(year, month, day, hour, minute, second, millisecond * 1000)

def get_end_timestamp(logs):
    global process_end_key_log
    timestamp = "Null"
    for log in logs:
        if process_end_key_log in str(log):
            timestamp = log.split(" [Info]", maxsplit=1)[0]
            timestamp = timestamp.replace("[", "")
            timestamp = timestamp.replace("]", "")
    # print("End Time:" + timestamp)
    return timestamp

def get_current_subject_name():
    script_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(script_path)
    folder_name = os.path.basename(folder_path)
    items = folder_name.split("_")
    subject_name = items[1]
    return subject_name

def get_proj_folder_name():
    script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(script_path)
    parent_folder = os.path.dirname(current_folder)
    grandparent_folder = os.path.dirname(parent_folder)
    return grandparent_folder

def dt_to_str(dt):
    format_str = "%Y_%m_%d_%H_%M_%S_%f"
    formatted_dt = dt.strftime(format_str)
    return formatted_dt[:-3]

if __name__ == "__main__":
    build_time_reference()
