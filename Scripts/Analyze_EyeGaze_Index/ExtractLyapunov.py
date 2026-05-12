import pandas as pd
import numpy as np
import os
import csv

target_level_tail = '_B5'

data = pd.read_csv('Lyapunov_Wolf.csv')

a1_data = data[data['level'].str.endswith(target_level_tail)]

subject_mle_dict = {}

group_security = []
group_passenger = []
group_robot = []

def get_grand_grand_parent_folder():
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    grandparent_folder = os.path.dirname(parent_folder)
    return grandparent_folder

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

def build_group_ref():
    global group_security
    global group_passenger
    global group_robot

    target_file_name = get_grand_grand_parent_folder() + os.sep + "Results" + os.sep + "Subject_Leader.csv"
    with open(target_file_name, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                name = row[0]
                if "Passenger" in str(row[3]):
                    group_passenger.append(name)
                if "Security" in str(row[3]):
                    group_security.append(name)
                if "Robot" in str(row[3]):
                    group_robot.append(name)
    print("Passenger组总计：" + str(len(group_passenger)))
    print("Security组总计：" + str(len(group_security)))
    print("Robot组总计：" + str(len(group_robot)))

def execute():
    for _, row in a1_data.iterrows():
        level_value = row['level']
        subject_name = level_value.split('_')[0]
        subject_mle_dict[subject_name] = row['Lyapunov值']

    print("受试者MLE值字典:")
    for subject, mle_value in subject_mle_dict.items():
        print(f"{subject}: {mle_value}")

    out_put_folder = "LyapunovData"
    if not os.path.exists(out_put_folder):
        os.mkdir(out_put_folder)

    with open(out_put_folder + os.sep + "Security" + target_level_tail + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
        for key in subject_mle_dict.keys():
            if key in group_security:
                csvfile.write(key + "," + str(subject_mle_dict[key]) + "\n")

    with open(out_put_folder + os.sep + "Passenger" + target_level_tail + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
        for key in subject_mle_dict.keys():
            if key in group_passenger:
                csvfile.write(key + "," + str(subject_mle_dict[key]) + "\n")

    with open(out_put_folder + os.sep + "Robot" + target_level_tail + ".csv", 'w', newline='', encoding='utf-8') as csvfile:
        for key in subject_mle_dict.keys():
            if key in group_robot:
                csvfile.write(key + "," + str(subject_mle_dict[key]) + "\n")

if __name__ == "__main__":
    build_group_ref()
    execute()
