import os
import openpyxl
import csv
from tqdm import tqdm

global_data_reference = {}
global_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

subject_dp_info_dicts = {}

log_key_word = "Subject Agent Has Arrive"
log_file_key_word = "Log_Info"

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
    global global_data_reference
    global subject_dp_info_dicts

    progress_bar = tqdm(total=len(global_data_reference))

    subject_data_index = 0
    while subject_data_index < len(global_data_reference.keys()):
        temp_ref_list = list(global_data_reference.keys())
        current_name_reference = temp_ref_list[subject_data_index]
        subject_folder_path = global_data_reference[current_name_reference]

        dp_infos = ""
        dp_infos = dp_infos + get_subject_dp(0, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(1, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(2, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(3, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(4, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(5, subject_folder_path) + ","
        dp_infos = dp_infos + get_subject_dp(6, subject_folder_path)

        subject_dp_info_dicts[current_name_reference] = dp_infos
        # print("Name: " + current_name_reference + " DP: " + dp_infos)

        progress_bar.update(1)
        progress_bar.set_description(f"提取受试者决策信息")
        subject_data_index = subject_data_index + 1

    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    output_target_file = parent_folder + os.sep + "Results" + os.sep + "Subject_DP.csv"

    csv_header = "SubjectName,A1,A2,B1,B2,B3,B4,B5"
    with open(output_target_file, mode='w', encoding='utf-8', newline='') as file:
        file.write(csv_header + "\n")
        for key in subject_dp_info_dicts.keys():
            line_content = key + "," + subject_dp_info_dicts[key]
            file.write(line_content + "\n")

def get_subject_dp(level, data_raw_path):
    global global_level_names

    level_data_dir = data_raw_path + os.sep + global_level_names[level]
    log_file_path = ""

    dir_files = get_all_file_paths(level_data_dir)

    result = "Error"

    if len(dir_files) == 0:
        result = "Null"
    else:
        for file in dir_files:
            if log_file_key_word in file:
                log_file_path = file
        with open(log_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if log_key_word in str(row[0]):
                    info_butt = str(row[0]).split("[Info]")[1]
                    dp = info_butt.replace("Subject Agent Has Arrive. Target_ID: ", "")
                    result = get_target_name(dp)

    return result

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def get_target_name(str_target_id):
    if str_target_id == "0":
        return "AL"
    if str_target_id == "1":
        return "AR"
    if str_target_id == "2":
        return "BL"
    if str_target_id == "3":
        return "BR"
    if str_target_id == "4":
        return "CL"
    if str_target_id == "5":
        return "CR"
    if str_target_id == "6":
        return "DL"
    if str_target_id == "7":
        return "DR"

if __name__ == "__main__":
    prepare()
    read_and_extract()
