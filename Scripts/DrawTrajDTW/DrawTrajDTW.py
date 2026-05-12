import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

target_levels = ["A2", "B1", "B2", "B3", "B4", "B5"]

group_security = []
group_passenger = []
group_robot = []

dtw_dict = {}

def get_grand_grand_parent_folder():
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    grandparent_folder = os.path.dirname(parent_folder)
    return grandparent_folder

def read_and_draw(level):
    global dtw_dict
    raw_dtw_data_path = get_grand_grand_parent_folder() + os.sep + "Results" + os.sep + "TrajDTW.csv"
    with open(raw_dtw_data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            # print(str(row))
            level_name = row[0]
            level_name = level_name.replace(".csv", "")
            level_dtw = float(row[1])
            dtw_dict[level_name] = level_dtw
    print("DTW data records found / 共检索到DTW数据量：" + str(len(dtw_dict.keys())))

    list_security = []
    list_passenger = []
    list_robot = []

    for key in dtw_dict.keys():
        subject_name = str(key).split("_")[0]
        subject_level = str(key).split("_")[1]
        subject_dtw = dtw_dict[key]
        # print(key)
        if subject_level == level:
            if subject_name in group_security:
                list_security.append(subject_dtw)
            if subject_name in group_passenger:
                list_passenger.append(subject_dtw)
            if subject_name in group_robot:
                list_robot.append(subject_dtw)

    print("Security data count / Security数据量：" + str(len(list_security)))
    print("Passenger data count / Passenger数据量:" + str(len(list_passenger)))
    print("Robot data count / Robot数据量：" + str(len(list_robot)))

    data = [list_security, list_passenger, list_robot]
    labels = ['Security', 'Passenger', 'Robot']

    means = [np.mean(group) for group in data]

    plt.figure(figsize=(16, 9))
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    plt.rcParams['figure.dpi'] = 600

    colors = ["#C4DFFF", "#FAE2D3", "#FFF5D3"]

    sns.violinplot(data=data, palette='Paired')

    plt.xticks(range(len(labels)), labels)

    bbox_props = dict(boxstyle="round", fc="w", ec="gray", alpha=0.8)
    for i, mean in enumerate(means):
        plt.text(i, mean, f'{mean:.2f}', ha='center', va='center', color='black', fontsize=12, bbox=bbox_props)

    plt.title('DTW Distribution  Level: ' + level)
    plt.ylabel('DTW Value')

    plt.ylim(bottom=0)

    plt.savefig(f'{level}_DTW.png', bbox_inches='tight')
    plt.close()

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
    print("Passenger group total / Passenger组总计：" + str(len(group_passenger)))
    print("Security group total / Security组总计：" + str(len(group_security)))
    print("Robot group total / Robot组总计：" + str(len(group_robot)))

if __name__ == "__main__":
    build_group_ref()
    for level in target_levels:
        read_and_draw(level)
