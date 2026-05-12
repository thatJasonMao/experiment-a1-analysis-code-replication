import os
import openpyxl
import datetime
from openpyxl import Workbook
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

global_data_reference = {}
global_level_names = ["A1", "A2", "B1", "B2", "B3", "B4", "B5"]

trajectory_a1 = trajectory_a2 = trajectory_b1 = trajectory_b2 = trajectory_b3 = trajectory_b4 = trajectory_b5 = []

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

def read_and_draw():
    global trajectory_a1, trajectory_a2, trajectory_b1, trajectory_b2, trajectory_b3, trajectory_b4, trajectory_b5

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

        current_script_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_script_path)
        parent_folder = os.path.dirname(current_folder)
        output_path = parent_folder + os.sep + "Results" + os.sep + "Figs" + os.sep + "Subject_Trajectory_Single" + os.sep + current_name_reference

        if not os.path.exists(output_path):
            os.mkdir(output_path)
        else:
            clear_path(output_path)

        level_index = 0
        while level_index < len(global_level_names):
            final_output_path = output_path + os.sep + global_level_names[level_index] + ".png"
            if level_index == 0:
                draw_fig(trajectory_a1, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 1:
                draw_fig(trajectory_a2, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 2:
                draw_fig(trajectory_b1, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 3:
                draw_fig(trajectory_b2, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 4:
                draw_fig(trajectory_b3, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 5:
                draw_fig(trajectory_b4, final_output_path, current_name_reference, global_level_names[level_index])
            if level_index == 6:
                draw_fig(trajectory_b5, final_output_path, current_name_reference, global_level_names[level_index])

            level_index = level_index + 1

        if will_pause_after_first_subject:
            quit()

        trajectory_a1.clear()
        trajectory_a2.clear()
        trajectory_b1.clear()
        trajectory_b2.clear()
        trajectory_b3.clear()
        trajectory_b4.clear()
        trajectory_b5.clear()

        subject_data_index = subject_data_index + 1

def draw_fig(data_list, path, name, level):
    if len(data_list) > 0:
        lst_x = []
        lst_y = []
        lst_z = []

        is_confirm_init = False

        point_index = 0
        while point_index < len(data_list):
            axis_datas = data_list[point_index].split(",")
            if float(axis_datas[1]) == -15.766:
                is_confirm_init = True

            if is_confirm_init:
                lst_x.append(float(axis_datas[0]))
                lst_z.append(float(axis_datas[1]))
                lst_y.append(float(axis_datas[2]))
            point_index = point_index + 1

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        dpi = 400
        width_inches = 2000 / dpi
        height_inches = 1600 / dpi

        fig = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(lst_x, lst_y, lst_z,
                marker='o',
                linestyle='-',
                linewidth=0.1,
                markersize=0.1,
                markeredgecolor='black',
                markerfacecolor='black')

        ax.set_box_aspect((4, 4, 1))

        ax.set_title('  Subject Trajectory: ' + name + '-' + level, pad=-15)

        plt.savefig(
            path,
            bbox_inches='tight',

            pad_inches=0.1

        )
        plt.close()

def clear_path(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except FileNotFoundError:
        print(f"指定的文件夹 {folder_path} 不存在。")
    except PermissionError:
        print(f"没有权限删除文件夹 {folder_path} 中的文件。")

def build_list(data_folder_path, level):
    global global_level_names
    global trajectory_a1, trajectory_a2, trajectory_b1, trajectory_b2, trajectory_b3, trajectory_b4, trajectory_b5

    target_list = []
    target_sub_folder_path = data_folder_path + os.sep + global_level_names[level]
    dir_files = get_all_file_paths(target_sub_folder_path)
    target_file = ""
    target_keyword = global_level_names[level] + "_Subject_Simulation_Info"
    for file in dir_files:
        if target_keyword in str(file):
            target_file = str(file)
    if os.path.exists(target_file):
        target_list = read_3d_coordinates(target_file)
    else:
        target_list = []

    if level == 0:
        trajectory_a1 = target_list
    if level == 1:
        trajectory_a2 = target_list
    if level == 2:
        trajectory_b1 = target_list
    if level == 3:
        trajectory_b2 = target_list
    if level == 4:
        trajectory_b3 = target_list
    if level == 5:
        trajectory_b4 = target_list
    if level == 6:
        trajectory_b5 = target_list

def read_3d_coordinates(csv_file_path):
    coordinates = []
    with open(csv_file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            if len(row) >= 4:
                x = row[1]
                y = row[2]
                z = row[3]
                coordinate_str = f"{x},{y},{z}"
                coordinates.append(coordinate_str)
    return coordinates

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths

if __name__ == "__main__":
    prepare()
    read_and_draw()
