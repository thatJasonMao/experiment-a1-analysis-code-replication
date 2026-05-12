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

        build_list_and_output(0, subject_folder_path, current_name_reference)
        build_list_and_output(1, subject_folder_path, current_name_reference)
        build_list_and_output(2, subject_folder_path, current_name_reference)
        build_list_and_output(3, subject_folder_path, current_name_reference)
        build_list_and_output(4, subject_folder_path, current_name_reference)
        build_list_and_output(5, subject_folder_path, current_name_reference)
        build_list_and_output(6, subject_folder_path, current_name_reference)

        progress_bar.update(1)
        progress_bar.set_description(f"提取受试者的眼动视场")

        subject_data_index = subject_data_index + 1

def build_list_and_output(level, data_raw_path, subject_name):
    global global_level_names
    level_data_dir = data_raw_path + os.sep + global_level_names[level]

    full_subject_infos = {}
    full_gaze_infos = {}

    subject_file_keyword = "Subject_Simulation_Info"
    gaze_file_key_word = "EyeGaze_Simulation_Info"

    subject_file_path = ""
    gaze_file_path = ""

    dir_files = get_all_file_paths(level_data_dir)
    if len(dir_files) == 0:
        full_subject_infos = {}
        full_gaze_infos = {}
    else:
        for file in dir_files:
            if subject_file_keyword in file:
                subject_file_path = file
            if gaze_file_key_word in file:
                gaze_file_path = file

        with open(subject_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) >= 4:
                    x = row[1]
                    y = row[2]
                    z = row[3]

                    rot_x = row[7]
                    rot_y = row[8]
                    rot_z = row[9]

                    info_str = f"{x},{y},{z},{rot_x},{rot_y},{rot_z}"
                    timestamp = row[0]
                    full_subject_infos[timestamp] = info_str
                    # print("Level: " + str(level) + " Time:" + timestamp + " Pos:" + info_str)

        with open(gaze_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) >= 4:
                    x = row[7]
                    y = row[8]
                    z = row[9]
                    coordinate_str = f"{x},{y},{z}"
                    timestamp = row[0]
                    full_gaze_infos[timestamp] = coordinate_str

        local_gaze_location = {}
        subject_side_time_stamps = list(full_subject_infos.keys())
        key_index = 0
        while key_index < len(subject_side_time_stamps):
            stamp = subject_side_time_stamps[key_index]
            if stamp in full_gaze_infos.keys():
                content = full_subject_infos[stamp] + "," + full_gaze_infos[stamp]
                local_gaze_location[stamp] = content
            key_index = key_index + 1

        current_script_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_script_path)
        parent_folder = os.path.dirname(current_folder)
        output_raw_path = parent_folder + os.sep + "Results" + os.sep + "Gaze_Field" + os.sep + subject_name
        output_target_file = parent_folder + os.sep + "Results" + os.sep + "Gaze_Field" + os.sep + subject_name + os.sep + global_level_names[level] + ".csv"
        if not os.path.exists(output_raw_path):
            os.mkdir(output_raw_path)

        csv_header = "TimeStamp,SubjectPosX,SubjectPosY,SubjectPosZ,SubjectRotX,SubjectRotY,SubjectRotZ,HitPosX,HitPosY,HitPosZ"
        with open(output_target_file, mode='w', encoding='utf-8', newline='') as file:
            file.write(csv_header + "\n")
            for key in local_gaze_location.keys():
                line_content = key + "," + local_gaze_location[key]
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
