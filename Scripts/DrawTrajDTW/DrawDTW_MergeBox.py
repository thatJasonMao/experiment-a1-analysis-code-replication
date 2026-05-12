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

def read_data():
    global dtw_dict
    raw_dtw_data_path = get_grand_grand_parent_folder() + os.sep + "Results" + os.sep + "TrajDTW.csv"
    with open(raw_dtw_data_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            level_name = row[0]
            level_name = level_name.replace(".csv", "")
            level_dtw = float(row[1])
            dtw_dict[level_name] = level_dtw
    print("共检索到DTW数据量：" + str(len(dtw_dict.keys())))

def get_data_by_level(level):
    list_security = []
    list_passenger = []
    list_robot = []

    for key in dtw_dict.keys():
        subject_name = str(key).split("_")[0]
        subject_level = str(key).split("_")[1]
        subject_dtw = dtw_dict[key]
        if subject_level == level:
            if subject_name in group_security:
                list_security.append(subject_dtw)
            if subject_name in group_passenger:
                list_passenger.append(subject_dtw)
            if subject_name in group_robot:
                list_robot.append(subject_dtw)

    print(f"{level} - Security数据量：" + str(len(list_security)))
    print(f"{level} - Passenger数据量:" + str(len(list_passenger)))
    print(f"{level} - Robot数据量：" + str(len(list_robot)))

    return [list_passenger, list_security, list_robot]

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

if __name__ == "__main__":
    build_group_ref()
    read_data()

    all_dtw_values = []
    level_data = {}
    for level in target_levels:
        data = get_data_by_level(level)
        level_data[level] = data
        if level == "A2":
            all_dtw_values.extend(data[0] + data[1] + data[2])
        else:
            for group in data:
                all_dtw_values.extend(group)
    global_ymax = max(all_dtw_values)

    fig, axes = plt.subplots(2, 3, figsize=(20, 15))
    plt.rcParams['figure.dpi'] = 600
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.size'] = 22

    labels = ['Passenger', 'Security', 'Robot']

    for i, level in enumerate(target_levels):
        row = i // 3
        col = i % 3
        ax = axes[row, col]

        data = get_data_by_level(level)

        if level == "A2":
            merged_data = [data[0] + data[1] + data[2]]
            current_labels = ['All Groups']
            means = [np.mean(merged_data[0])]
        else:
            merged_data = data
            current_labels = labels
            means = [np.mean(group) for group in data]

        with open(f'mean/{level}_mean.csv', 'w', newline='', encoding='utf-8') as mean_file, \
             open(f'detail/{level}_detail.csv', 'w', newline='', encoding='utf-8') as detail_file:

            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerows(zip(labels, means))

            detail_writer = csv.writer(detail_file)
            detail_writer.writerow(['Group', 'DTW_Value'])
            for group_idx, group_name in enumerate(labels):
                detail_writer.writerows([[group_name, value] for value in data[group_idx]])

        sns.boxplot(data=merged_data, palette='coolwarm', ax=ax)
        sns.stripplot(data=merged_data, color='black', alpha=0.5, ax=ax)
        ax.set_xticklabels(current_labels, fontsize=22)

        bbox_props = dict(boxstyle="round", fc="w", ec="gray", alpha=0.8)
        for j, mean in enumerate(means):
            ax.set_ylim(0, global_ymax)

            ax.tick_params(axis='y', labelsize=22)
            ax.text(j, mean, f'{mean:.2f}', ha='center', va='center', color='black', fontsize=22, bbox=bbox_props)
            ax.set_title(f'Scenario: {level}')
            ax.set_ylabel('DTW Value', fontsize=22)

            ax.tick_params(axis='y', labelsize=22)

            ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig('all_levels_DTW.png', bbox_inches='tight')
    plt.close()
