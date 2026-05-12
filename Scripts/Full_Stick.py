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

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

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
        progress_bar.set_description(f"提取受试者摇杆输入")

        subject_data_index = subject_data_index + 1

def build_list(level, data_raw_path, subject_name):
    global global_level_names
    level_data_dir = data_raw_path + os.sep + global_level_names[level]

    stick_dict = {}
    subject_file_path = ""
    subject_file_key_word = "Subject_Simulation_Info"

    dir_files = get_all_file_paths(level_data_dir)
    if len(dir_files) == 0:
        stick_dict = {}
    else:
        for file in dir_files:
            if subject_file_key_word in file:
                subject_file_path = file

        with open(subject_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) > 0:
                    try:
                        stick_x = row[14]
                        stick_y = row[15]
                        stick_input = f"{stick_x},{stick_y}"
                        timestamp = row[0]
                        stick_dict[timestamp] = stick_input

                    except:
                        print("Error-Name:" + subject_name + " Level:" + str(level))

        current_script_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_script_path)
        parent_folder = os.path.dirname(current_folder)
        output_raw_path = parent_folder + os.sep + "Results" + os.sep + "Full_Stick" + os.sep + subject_name
        if not os.path.exists(output_raw_path):
            os.mkdir(output_raw_path)
        output_target_file = (parent_folder + os.sep + "Results" + os.sep + "Full_Stick"
                              + os.sep + subject_name + os.sep + global_level_names[level] + ".csv")

        csv_header = "TimeStamp,Stick_X,Stick_Y"
        with open(output_target_file, mode='w', encoding='utf-8', newline='') as file:
            file.write(csv_header + "\n")
            for key in stick_dict.keys():
                line_content = key + "," + stick_dict[key]
                file.write(line_content + "\n")

if __name__ == "__main__":
    prepare()
    read_and_extract()
