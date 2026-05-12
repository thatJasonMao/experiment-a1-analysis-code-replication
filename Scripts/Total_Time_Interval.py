import os
import openpyxl
import csv
from datetime import datetime

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
    upstream_time_data_dict = {}
    subject_time_interval = {}

    subject_l0 = {}
    subject_l1 = {}
    subject_l2 = {}
    subject_l3 = {}
    subject_l4 = {}
    subject_l5 = {}
    subject_l6 = {}

    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    upstream_time_file_path = parent_folder + os.sep + "Results" + os.sep + "Subject_Total_Travel_Time.csv"
    with open(upstream_time_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) > 0:
                subject_name = row[0]
                subject_key_time = ""
                row_inner_index = 1
                while row_inner_index <= 14:
                    subject_key_time = subject_key_time + row[row_inner_index] + ","
                    row_inner_index = row_inner_index + 1
                # print(subject_name)
                # print(subject_key_time)
                upstream_time_data_dict[subject_name] = subject_key_time
    print("源数据总计：" + str(len(upstream_time_data_dict)))

    subject_data_index = 0
    while subject_data_index < len(global_data_reference.keys()):
        temp_ref_list = list(global_data_reference.keys())
        current_name_reference = temp_ref_list[subject_data_index]
        raw_data = upstream_time_data_dict[current_name_reference]

        l0 = calculate_time(raw_data, 0)
        subject_l0[current_name_reference] = l0

        l1 = calculate_time(raw_data, 1)
        subject_l1[current_name_reference] = l1

        l2 = calculate_time(raw_data, 2)
        subject_l2[current_name_reference] = l2

        l3 = calculate_time(raw_data, 3)
        subject_l3[current_name_reference] = l3

        l4 = calculate_time(raw_data, 4)
        subject_l4[current_name_reference] = l4

        l5 = calculate_time(raw_data, 5)
        subject_l5[current_name_reference] = l5

        l6 = calculate_time(raw_data, 6)
        subject_l6[current_name_reference] = l6

        subject_data_index = subject_data_index + 1

    out_put(subject_l0, 0)
    out_put(subject_l1, 1)
    out_put(subject_l2, 2)
    out_put(subject_l3, 3)
    out_put(subject_l4, 4)
    out_put(subject_l5, 5)
    out_put(subject_l6, 6)

def calculate_time(raw_data, level):
    interval = "Null"
    datas = raw_data.split(',')
    start_time = datas[level]
    end_time = datas[level + 7]
    if start_time != "Null" and end_time != "Null":
        t1 = text_timestamp_to_datetime(start_time)
        # print("t1:" + str(t1))
        t2 = text_timestamp_to_datetime(end_time)
        # print("t2:" + str(t2))
        interval = str(abs(t2 - t1).total_seconds())
    return interval

def text_timestamp_to_datetime(text_timestamp):
    parts = text_timestamp.split('_')
    year, month, day, hour, minute, second, millisecond = map(int, parts)
    return datetime(year, month, day, hour, minute, second, millisecond * 1000)

def out_put(container, level):
    global global_level_names
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    output_path = parent_folder + os.sep + "Results" + os.sep + "Travel_Time_Interval_" + global_level_names[level] + ".csv"
    csv_header = "SubjectName,TravelTimeInterval"
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        file.write(csv_header + "\n")
        for key in container.keys():
            line_content = key + "," + container[key]
            file.write(line_content + "\n")

if __name__ == "__main__":
    prepare()
    read_and_extract()
