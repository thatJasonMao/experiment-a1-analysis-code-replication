import os
import openpyxl
import datetime
from openpyxl import Workbook
import csv
from tqdm import tqdm

process_start_key_log = "Unfreeze Subject Agent Move"
process_end_key_log = "Subject Agent Has Arrive"

start_timestamp_dicts = {}
end_timestamp_dicts = {}

global_data_reference = {}
global_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

infos_a1 = infos_a2 = infos_b1 = infos_b2 = infos_b3 = infos_b4 = infos_b5 = []

will_pause_after_first_subject = False

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
    global infos_a1, infos_a2, infos_b1, infos_b2, infos_b3, infos_b4, infos_b5
    global global_data_reference

    global start_timestamp_dicts
    global end_timestamp_dicts

    progress_bar = tqdm(total=len(global_data_reference))

    subject_data_index = 0
    while subject_data_index < len(global_data_reference.keys()):
        temp_ref_list = list(global_data_reference.keys())
        current_name_reference = temp_ref_list[subject_data_index]
        subject_folder_path = global_data_reference[current_name_reference]

        build_list(subject_folder_path, 0)
        build_list(subject_folder_path, 1)
        build_list(subject_folder_path, 2)
        build_list(subject_folder_path, 3)
        build_list(subject_folder_path, 4)
        build_list(subject_folder_path, 5)
        build_list(subject_folder_path, 6)

        progress_bar.update(1)
        progress_bar.set_description(f"处理并绘制受试者数据")

        if will_pause_after_first_subject:
            quit()

        start_time_stamps = ""
        start_time_stamps = start_time_stamps + get_start_timestamp(infos_a1)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_a2)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_b1)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_b2)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_b3)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_b4)
        start_time_stamps = start_time_stamps + "," + get_start_timestamp(infos_b5)
        start_timestamp_dicts[current_name_reference] = start_time_stamps

        end_time_stamps = ""
        end_time_stamps = end_time_stamps + get_end_timestamp(infos_a1)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_a2)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_b1)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_b2)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_b3)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_b4)
        end_time_stamps = end_time_stamps + "," + get_end_timestamp(infos_b5)
        end_timestamp_dicts[current_name_reference] = end_time_stamps

        infos_a1.clear()
        infos_a2.clear()
        infos_b1.clear()
        infos_b2.clear()
        infos_b3.clear()
        infos_b4.clear()
        infos_b5.clear()

        subject_data_index = subject_data_index + 1

def build_list(data_folder_path, level):
    global global_level_names
    global infos_a1, infos_a2, infos_b1, infos_b2, infos_b3, infos_b4, infos_b5

    target_list = []
    target_file = ""

    target_sub_folder_path = data_folder_path + os.sep + global_level_names[level]
    dir_files = get_all_file_paths(target_sub_folder_path)
    target_keyword = global_level_names[level] + "_Log_Info"
    if len(dir_files) > 0:
        for file in dir_files:
            if target_keyword in str(file):
                target_file = str(file)
                target_list = read_log_content(target_file)
    else:
        target_list = []

    # print("Current Level: " + str(level) + " Data Length: " + str(len(target_list)))

    if level == 0:
        infos_a1 = target_list
    if level == 1:
        infos_a2 = target_list
    if level == 2:
        infos_b1 = target_list
    if level == 3:
        infos_b2 = target_list
    if level == 4:
        infos_b3 = target_list
    if level == 5:
        infos_b4 = target_list
    if level == 6:
        infos_b5 = target_list

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

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

def read_log_content(log_file_path):
    contents = []
    with open(log_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 1:
                contents.append(row[0])
    return contents

def output():
    global start_timestamp_dicts
    global end_timestamp_dicts
    global global_data_reference
    for name in global_data_reference.keys():
        temp_content = "ID:" + name + " Start:" + start_timestamp_dicts[name] + "End:" + end_timestamp_dicts[name]
        print(temp_content)

    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    output_path = parent_folder + os.sep + "Results" + os.sep + "Subject_Total_Travel_Time.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    csv_header = "Name,Start_A1,Start_A2,Start_B1,Start_B2,Start_B3,Start_B4,Start_B5,End_A1,End_A2,End_B1,End_B2,End_B3,End_B4,End_B5"
    with open(output_path, 'w', encoding='utf-8', newline='') as file:
        file.write(csv_header + "\n")
        for key in global_data_reference.keys():
            line_content = key + "," + start_timestamp_dicts[key] + "," + end_timestamp_dicts[key] + ","
            file.write(line_content + "\n")

if __name__ == "__main__":
    prepare()
    read_and_extract()
    output()
