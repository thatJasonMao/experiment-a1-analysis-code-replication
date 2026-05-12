import os
import csv

group_security = []
group_passenger = []
group_robot = []

total_distance_infos = []

def build_group_ref():
    global group_security
    global group_passenger
    global group_robot

    target_file_name = get_parent_folder_path() + os.sep + "Results" + os.sep + "Subject_Leader.csv"
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
    print("Passenger group total / Passenger组总计：" + str(len(group_passenger)))
    print("Security group total / Security组总计：" + str(len(group_security)))
    print("Robot group total / Robot组总计：" + str(len(group_robot)))

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

def build_csv(lines, path):
    with open(path,'w', newline='', encoding='utf-8') as csvfile:
        for line in lines:
            csvfile.write(line + "\n")

def extract_distance_by_group():
    global total_distance_infos
    target_file_path = get_parent_folder_path() + os.sep + "GroupData_Total_Move_Distance" + os.sep + "Result.csv"
    with open(target_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                total_distance_infos.append(row)
    print("Total Level Distance Count:" + str(len(total_distance_infos)))
    output_group_security(get_parent_folder_path() + os.sep + "GroupData_Total_Move_Distance")
    output_group_passenger(get_parent_folder_path() + os.sep + "GroupData_Total_Move_Distance")
    output_group_robot(get_parent_folder_path() + os.sep + "GroupData_Total_Move_Distance")

def output_group_security(path):
    global total_distance_infos
    global group_security

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_security:
        for line in total_distance_infos:
            if name in str(line[0]):
                level_name = line[0].split("_")[1]
                content = str(name) + "," + str(line[1])
                if level_name == "A1":
                    a1.append(content)
                if level_name == "A2":
                    a2.append(content)
                if level_name == "B1":
                    b1.append(content)
                if level_name == "B2":
                    b2.append(content)
                if level_name == "B3":
                    b3.append(content)
                if level_name == "B4":
                    b4.append(content)
                if level_name == "B5":
                    b5.append(content)

    build_csv(a1, path + os.sep + "Security_A1.csv")
    build_csv(a2, path + os.sep + "Security_A2.csv")
    build_csv(b1, path + os.sep + "Security_B1.csv")
    build_csv(b2, path + os.sep + "Security_B2.csv")
    build_csv(b3, path + os.sep + "Security_B3.csv")
    build_csv(b4, path + os.sep + "Security_B4.csv")
    build_csv(b5, path + os.sep + "Security_B5.csv")

def output_group_passenger(path):
    global total_distance_infos
    global group_passenger

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_passenger:
        for line in total_distance_infos:
            if name in str(line[0]):
                level_name = line[0].split("_")[1]
                content = str(name) + "," + str(line[1])
                if level_name == "A1":
                    a1.append(content)
                if level_name == "A2":
                    a2.append(content)
                if level_name == "B1":
                    b1.append(content)
                if level_name == "B2":
                    b2.append(content)
                if level_name == "B3":
                    b3.append(content)
                if level_name == "B4":
                    b4.append(content)
                if level_name == "B5":
                    b5.append(content)

    build_csv(a1, path + os.sep + "Passenger_A1.csv")
    build_csv(a2, path + os.sep + "Passenger_A2.csv")
    build_csv(b1, path + os.sep + "Passenger_B1.csv")
    build_csv(b2, path + os.sep + "Passenger_B2.csv")
    build_csv(b3, path + os.sep + "Passenger_B3.csv")
    build_csv(b4, path + os.sep + "Passenger_B4.csv")
    build_csv(b5, path + os.sep + "Passenger_B5.csv")

def output_group_robot(path):
    global total_distance_infos
    global group_robot

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_robot:
        for line in total_distance_infos:
            if name in str(line[0]):
                level_name = line[0].split("_")[1]
                content = str(name) + "," + str(line[1])
                if level_name == "A1":
                    a1.append(content)
                if level_name == "A2":
                    a2.append(content)
                if level_name == "B1":
                    b1.append(content)
                if level_name == "B2":
                    b2.append(content)
                if level_name == "B3":
                    b3.append(content)
                if level_name == "B4":
                    b4.append(content)
                if level_name == "B5":
                    b5.append(content)

    build_csv(a1, path + os.sep + "Robot_A1.csv")
    build_csv(a2, path + os.sep + "Robot_A2.csv")
    build_csv(b1, path + os.sep + "Robot_B1.csv")
    build_csv(b2, path + os.sep + "Robot_B2.csv")
    build_csv(b3, path + os.sep + "Robot_B3.csv")
    build_csv(b4, path + os.sep + "Robot_B4.csv")
    build_csv(b5, path + os.sep + "Robot_B5.csv")

if __name__ == "__main__":
    build_group_ref()
    extract_distance_by_group()
