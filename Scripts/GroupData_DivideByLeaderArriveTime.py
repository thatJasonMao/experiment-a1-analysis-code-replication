import os
import csv
import openpyxl

level_names = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']

raw_data_paths = []
dp_2_times = {}
dp_3_times = {}
subject_level_names = []

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
    global raw_data_paths
    raw_data_file = get_parent_folder_path() + os.sep + "Subject_Data_Global_Reference.xlsx"
    if os.path.exists(raw_data_file):
        # print(raw_data_file)
        workbook = openpyxl.load_workbook(raw_data_file)
        sheet = workbook.active
        column_f = []
        for row in sheet.iter_rows(min_row=1, min_col=6, max_col=6, values_only=True):
            column_f.append(row[0])
        for value in column_f:
            if str(value) != "Null" and str(value) != "数据路径":
                raw_data_paths.append(str(value))
        workbook.close()
        print("共统计到数据路径数量：" + str(len(raw_data_paths)))

        for path in raw_data_paths:
            get_dp_time_by_subject(path)

def get_dp_time_by_subject(path):
    for level in level_names:
        get_dp_time_by_level(path, level)

def read_log_content(log_file_path):
    contents = []
    with open(log_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 1:
                contents.append(row[0])
    return contents

def get_dp2_timestamp(logs):
    dp2_key_log = "Leader Trigger DP2"
    timestamp = "Null"
    for log in logs:
        if dp2_key_log in str(log):
            timestamp = log.split(" [Info]", maxsplit=1)[0]
            timestamp = timestamp.replace("[", "")
            timestamp = timestamp.replace("]", "")
    # print("Start Time:" + timestamp)
    return timestamp

def get_dp3_timestamp(logs):
    dp3_key_log = "Leader Trigger DP3"
    timestamp = "Null"
    for log in logs:
        if dp3_key_log in str(log):
            timestamp = log.split(" [Info]", maxsplit=1)[0]
            timestamp = timestamp.replace("[", "")
            timestamp = timestamp.replace("]", "")
    # print("Start Time:" + timestamp)
    return timestamp

def get_dp_time_by_level(path, level):
    global dp_2_times
    global dp_3_times
    global subject_level_names

    target_sub_folder_path = path + os.sep + level
    if os.path.exists(target_sub_folder_path):
        files = get_all_file_paths(target_sub_folder_path)
        if len(files) != 4:
            print("Error! Unexpected File Length. Target Path:" + target_sub_folder_path)
        else:
            for file in files:
                file_name = os.path.basename(file)
                if "Log_Info" in file_name:
                    log_contents = read_log_content(file)
                    dp_2 = get_dp2_timestamp(log_contents)
                    dp_3 = get_dp3_timestamp(log_contents)
                    folder_name = path.split("\\")[len(path.split("\\")) - 1]
                    subject_name = folder_name.split("_")[1]
                    print(subject_name + " Level:" + level + " DP2:" + dp_2 + " DP3:" + dp_3)
                    key = subject_name + "_" + level
                    subject_level_names.append(key)
                    dp_2_times[key] = dp_2
                    dp_3_times[key] = dp_3

def out_put():
    global dp_2_times
    global dp_3_times
    global subject_level_names

    header = "Level,DP2_Time,DP3_Time"
    output_path = get_parent_folder_path() + os.sep + "Results" + os.sep + "Leader_Arrive_DP_Time.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for key in subject_level_names:
            item_0 = key
            item_1 = dp_2_times[key]
            item_2 = dp_3_times[key]
            line = item_0 + "," + item_1 + "," + item_2
            csvfile.write(line + "\n")

if __name__ == "__main__":
    divide_by_time()
    out_put()
