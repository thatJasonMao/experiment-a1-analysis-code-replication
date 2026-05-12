import os
import csv
from tqdm import tqdm

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

def get_gaze_on_all(path):
    gaze_info_lines = []
    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                time_stamp = row[0]
                subject_pos = row[1] + "," + row[2] + "," + row[3]
                subject_rot = row[7] + "," + row[8] + "," + row[9]
                gaze_pos = row[22] + "," + row[23] + "," + row[24]
                new_line = time_stamp + "," + subject_pos + "," + subject_rot + "," + gaze_pos
                gaze_info_lines.append(new_line)

    output_folder = get_parent_folder_path() + os.sep + "GroupData_Gaze_On_All"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + str(level_name) + ".csv"
    header = "TimeStamp,SubjectPosX,SubjectPosY,SubjectPosZ,SubjectRotX,SubjectRotY,SubjectRotZ,GazePX,GazePY,GazePZ"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for line in gaze_info_lines:
            csvfile.write(line + "\n")

def analyze():
    target_folder = get_parent_folder_path() + os.sep + "GroupData"
    target_files = get_all_file_paths(target_folder)
    progress_bar = tqdm(total=len(target_files))
    for file in target_files:
        get_gaze_on_all(file)
        progress_bar.update(1)
        progress_bar.set_description(f"提取受试者对总体环境的注视")

if __name__ == "__main__":
    analyze()
