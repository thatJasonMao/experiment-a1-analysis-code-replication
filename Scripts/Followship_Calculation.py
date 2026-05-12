import os
import openpyxl
import csv
from tqdm import tqdm

global_data_reference = {}
global_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

will_pause_after_first_subject = True

def prepare():
    global global_data_reference

    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    config_table_path = parent_folder + os.sep + "Subject_Data_Global_Reference.xlsx"
    if not os.path.exists(config_table_path):
        print(">>Error! Config Path Is Null.")
        os.system("pause")

    workbook = openpyxl.load_workbook(config_table_path)
    sheet = workbook.active
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[2] is not None:
            if row[5] is not None:
                if row[5] != "Null":
                    global_data_reference[str(row[2])] = str(row[5])

    # print(global_data_reference)

def read_and_extract():
    progress_bar = tqdm(total=len(global_data_reference))

    subject_data_index = 0
    while subject_data_index < len(global_data_reference.keys()):
        temp_ref_list = list(global_data_reference.keys())
        current_name_reference = temp_ref_list[subject_data_index]
        subject_folder_path = global_data_reference[current_name_reference]

        build_list(0, subject_folder_path, current_name_reference)
        build_list(1, subject_folder_path, current_name_reference)
        build_list(2, subject_folder_path, current_name_reference)
        build_list(3, subject_folder_path, current_name_reference)
        build_list(4, subject_folder_path, current_name_reference)
        build_list(5, subject_folder_path, current_name_reference)
        build_list(6, subject_folder_path, current_name_reference)

        progress_bar.update(1)
        progress_bar.set_description(f"提取跟随关系")

        subject_data_index = subject_data_index + 1

def build_list(level, data_raw_path, subject_name):
    global global_level_names

    subject_container = {}
    leader_container = {}

    level_data_dir = data_raw_path + os.sep + global_level_names[level]

    subject_data_keyword = "Subject_Simulation_Info"
    npc_data_keyword = "NPC_Simulation_Info"

    subject_data_file = ""
    npc_data_file = ""

    dir_files = get_all_file_paths(level_data_dir)
    if len(dir_files) == 0:
        subject_container = {}
        leader_container = {}
    else:
        for file in dir_files:
            if subject_data_keyword in file:
                subject_data_file = file
            if npc_data_keyword in file:
                npc_data_file = file

        with open(subject_data_file, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) >= 4:
                    x = row[1]
                    y = row[2]
                    z = row[3]
                    coordinate_str = f"{x},{y},{z}"
                    timestamp = row[0]
                    subject_container[timestamp] = coordinate_str
                    # print("Level: " + str(level) + " Time:" + timestamp + " Pos:" + coordinate_str)

        with open(npc_data_file, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) >= 5:
                    if "Leader" in str(row[1]):
                        x = row[2]
                        y = row[3]
                        z = row[4]
                        coordinate_str = f"{x},{y},{z}"
                        timestamp = row[0]
                        leader_container[timestamp] = coordinate_str
                        # print("Level: " + str(level) + " Time:" + timestamp + " Pos:" + coordinate_str)

    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    output_raw_path = parent_folder + os.sep + "Results" + os.sep + "FollowShip" + os.sep + subject_name
    output_target_file = parent_folder + os.sep + "Results" + os.sep + "FollowShip" + os.sep + subject_name + os.sep + global_level_names[level] + ".csv"
    if not os.path.exists(output_raw_path):
        os.mkdir(output_raw_path)
    # print(output_raw_path)

    follow_ship = {}
    subject_side_time_stamps = list(subject_container.keys())
    key_index = 0
    while key_index < len(subject_side_time_stamps):
        stamp = subject_side_time_stamps[key_index]
        if stamp in leader_container.keys():
            content = subject_container[stamp] + "," + leader_container[stamp]
            follow_ship[stamp] = content
        key_index = key_index + 1

    csv_header = "TimeStamp,SubjectPosX,SubjectPosY,SubjectPosZ,LeaderPosX,LeaderPosY,LeaderPosZ"
    with open(output_target_file, mode='w', encoding='utf-8', newline='') as file:
        file.write(csv_header + "\n")
        for key in follow_ship.keys():
            line_content = key + "," + follow_ship[key]
            file.write(line_content + "\n")

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def clear_path(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except FileNotFoundError:
        print(f"Specified folder does not exist / 指定的文件夹 {folder_path} 不存在。")
    except PermissionError:
        print(f"No permission to delete files in folder / 没有权限删除文件夹 {folder_path} 中的文件。")

if __name__ == "__main__":
    prepare()
    read_and_extract()
