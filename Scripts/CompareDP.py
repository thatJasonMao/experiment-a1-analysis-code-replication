import os
import csv

group_security = []
group_passenger = []
group_robot = []

infos = []

sub_folder = "GroupData_Subject_DP"

leader_dp_1 = "AB"
leader_dp_2 = "A"
leader_dp_3 = "AR"

def get_follow_state(dp):
    result = "Null"

    if get_dp_1(dp) == leader_dp_1:
        result = result + "Follow" + ","
    else:
        result = result + "Escape" + ","

    if get_dp_2(dp) == leader_dp_2:
        result = result + "Follow" + ","
    else:
        result = result + "Escape" + ","

    if dp == leader_dp_3:
        result = result + "Follow" + ","
    else:
        result = result + "Escape" + ","

    return result

def get_dp_1(dp):
    result = "Null"

    if "A" in dp or "B" in dp:
        result = "AB"
    if "C" in dp or "D" in dp:
        result = "CD"

    return result

def get_dp_2(dp):
    result = "Null"

    if "A" in dp:
        result = "A"
    if "B" in dp:
        result = "B"
    if "C" in dp:
        result = "C"
    if "D" in dp:
        result = "D"

    return result

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
    print("Passenger组总计：" + str(len(group_passenger)))
    print("Security组总计：" + str(len(group_security)))
    print("Robot组总计：" + str(len(group_robot)))

def build_csv(lines, path):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        for line in lines:
            csvfile.write(line + "\n")

def get_parent_folder_path():
    current_script_path = os.path.abspath(__file__)
    current_folder_path = os.path.dirname(current_script_path)
    parent_folder_path = os.path.dirname(current_folder_path)
    return parent_folder_path

def extract_dp_by_group():
    global infos
    target_file_path = get_parent_folder_path() + os.sep + "Results" + os.sep + "Subject_DP.csv"
    with open(target_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                infos.append(row)
    print("Total Level Speed Count:" + str(len(infos)))
    # print(infos)

    if not os.path.exists(get_parent_folder_path() + os.sep + sub_folder):
        os.mkdir(get_parent_folder_path() + os.sep + sub_folder)

    output_group_security(get_parent_folder_path() + os.sep + sub_folder)
    output_group_passenger(get_parent_folder_path() + os.sep + sub_folder)
    output_group_robot(get_parent_folder_path() + os.sep + sub_folder)

def output_group_security(path):
    global infos
    global group_security

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_security:
        for line in infos:
            if name in str(line[0]):
                name = str(line[0])
                a1.append(name + "," + line[1] + "," + get_follow_state(line[1]))
                a2.append(name + "," + line[2] + "," + get_follow_state(line[2]))
                b1.append(name + "," + line[3] + "," + get_follow_state(line[3]))
                b2.append(name + "," + line[4] + "," + get_follow_state(line[4]))
                b3.append(name + "," + line[5] + "," + get_follow_state(line[5]))
                b4.append(name + "," + line[6] + "," + get_follow_state(line[6]))
                b5.append(name + "," + line[7] + "," + get_follow_state(line[7]))

    build_csv(a1, path + os.sep + "Security_A1.csv")
    build_csv(a2, path + os.sep + "Security_A2.csv")
    build_csv(b1, path + os.sep + "Security_B1.csv")
    build_csv(b2, path + os.sep + "Security_B2.csv")
    build_csv(b3, path + os.sep + "Security_B3.csv")
    build_csv(b4, path + os.sep + "Security_B4.csv")
    build_csv(b5, path + os.sep + "Security_B5.csv")

def output_group_passenger(path):
    global infos
    global group_passenger

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_passenger:
        for line in infos:
            if name in str(line[0]):
                name = str(line[0])
                a1.append(name + "," + line[1] + "," + get_follow_state(line[1]))
                a2.append(name + "," + line[2] + "," + get_follow_state(line[2]))
                b1.append(name + "," + line[3] + "," + get_follow_state(line[3]))
                b2.append(name + "," + line[4] + "," + get_follow_state(line[4]))
                b3.append(name + "," + line[5] + "," + get_follow_state(line[5]))
                b4.append(name + "," + line[6] + "," + get_follow_state(line[6]))
                b5.append(name + "," + line[7] + "," + get_follow_state(line[7]))

    build_csv(a1, path + os.sep + "Passenger_A1.csv")
    build_csv(a2, path + os.sep + "Passenger_A2.csv")
    build_csv(b1, path + os.sep + "Passenger_B1.csv")
    build_csv(b2, path + os.sep + "Passenger_B2.csv")
    build_csv(b3, path + os.sep + "Passenger_B3.csv")
    build_csv(b4, path + os.sep + "Passenger_B4.csv")
    build_csv(b5, path + os.sep + "Passenger_B5.csv")

def output_group_robot(path):
    global infos
    global group_robot

    a1 = []
    a2 = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []

    for name in group_robot:
        for line in infos:
            if name in str(line[0]):
                name = str(line[0])
                a1.append(name + "," + line[1] + "," + get_follow_state(line[1]))
                a2.append(name + "," + line[2] + "," + get_follow_state(line[2]))
                b1.append(name + "," + line[3] + "," + get_follow_state(line[3]))
                b2.append(name + "," + line[4] + "," + get_follow_state(line[4]))
                b3.append(name + "," + line[5] + "," + get_follow_state(line[5]))
                b4.append(name + "," + line[6] + "," + get_follow_state(line[6]))
                b5.append(name + "," + line[7] + "," + get_follow_state(line[7]))

    build_csv(a1, path + os.sep + "Robot_A1.csv")
    build_csv(a2, path + os.sep + "Robot_A2.csv")
    build_csv(b1, path + os.sep + "Robot_B1.csv")
    build_csv(b2, path + os.sep + "Robot_B2.csv")
    build_csv(b3, path + os.sep + "Robot_B3.csv")
    build_csv(b4, path + os.sep + "Robot_B4.csv")
    build_csv(b5, path + os.sep + "Robot_B5.csv")

if __name__ == "__main__":
    build_group_ref()
    extract_dp_by_group()
