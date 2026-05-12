import os
import openpyxl
import datetime
from openpyxl import Workbook

global_data_reference = {}
static_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

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

    print(">>共统计到路径映射：" + str(len(global_data_reference)))
    print(global_data_reference)

def read():
    print()

def output():
    print()

if __name__ == "__main__":
    prepare()
    read()
    output()
