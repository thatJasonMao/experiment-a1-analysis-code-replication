import os
import openpyxl
import csv
from tqdm import tqdm

global_data_reference = {}
global_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

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
        progress_bar.set_description(f"提取溅落在NPC身上的眼动点")

        subject_data_index = subject_data_index + 1

def build_list(level, data_raw_path, subject_name):
    global global_level_names
    level_data_dir = data_raw_path + os.sep + global_level_names[level]

    on_npc_gaze_data = {}
    gaze_file_path = ""
    gaze_file_keyword = "EyeGaze_Simulation"

    dir_files = get_all_file_paths(level_data_dir)
    if len(dir_files) == 0:
        on_npc_gaze_data = {}
    else:
        for file in dir_files:
            if gaze_file_keyword in file:
                gaze_file_path = file

        with open(gaze_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) > 0:
                    if "NPC" in str(row[10]):
                        x = row[7]
                        y = row[8]
                        z = row[9]
                        name = row[10]
                        hit_info = f"{x},{y},{z},{name}"
                        timestamp = row[0]
                        on_npc_gaze_data[timestamp] = hit_info

        current_script_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_script_path)
        parent_folder = os.path.dirname(current_folder)
        output_raw_path = parent_folder + os.sep + "Results" + os.sep + "Gaze_On_NPC" + os.sep + subject_name
        if not os.path.exists(output_raw_path):
            os.mkdir(output_raw_path)
        output_target_file = (parent_folder + os.sep + "Results" + os.sep + "Gaze_On_NPC"
                              + os.sep + subject_name + os.sep + global_level_names[level] + ".csv")

        csv_header = "TimeStamp,HitPosX,HitPosY,HitPosZ,HitObjName"
        with open(output_target_file, mode='w', encoding='utf-8', newline='') as file:
            file.write(csv_header + "\n")
            for key in on_npc_gaze_data.keys():
                line_content = key + "," + on_npc_gaze_data[key]
                file.write(line_content + "\n")

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

if __name__ == "__main__":
    prepare()
    read_and_extract()
