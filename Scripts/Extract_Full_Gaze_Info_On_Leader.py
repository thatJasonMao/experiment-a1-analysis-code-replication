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

def get_gaze_on_leader(path):
    gaze_info_lines = []
    file_name = os.path.basename(path)
    level_name = file_name.replace(".csv", "")
    with open(path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                if "Leader" in str(row[25]):
                    time_stamp = row[0]
                    subject_pos = row[1] + "," + row[2] + "," + row[3]
                    subject_rot = row[7] + "," + row[8] + "," + row[9]
                    leader_pos = row[35] + "," + row[36] + "," + row[37]
                    new_line = time_stamp + "," + subject_pos + "," + subject_rot + "," + leader_pos
                    if "Leader" not in str(row[34]):
                        print("Error! Leader Info Not Locate Correctly.")
                        print("Current Level:" + str(level_name) + " Time:" + time_stamp)
                        # os.system("pause")
                    else:
                        gaze_info_lines.append(new_line)

    output_folder = get_parent_folder_path() + os.sep + "GroupData_Gaze_On_Leader_Full_Info_Polar"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + str(level_name) + ".csv"
    header = "TimeStamp,SubjectPosX,SubjectPosY,SubjectPosZ,SubjectRotX,SubjectRotY,SubjectRotZ,LeaderPX,LeaderPY,LeaderPZ"
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvfile.write(header + "\n")
        for line in gaze_info_lines:
            csvfile.write(line + "\n")

def analyze():
    target_folder = get_parent_folder_path() + os.sep + "GroupData"
    target_files = get_all_file_paths(target_folder)
    progress_bar = tqdm(total=len(target_files))
    for file in target_files:
        get_gaze_on_leader(file)
        progress_bar.update(1)
        progress_bar.set_description(f"Extracting subject gaze on leader / 提取受试者对领导者的注视")

if __name__ == "__main__":
    analyze()
