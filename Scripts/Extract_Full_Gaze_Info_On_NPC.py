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
                if "NPC" in str(row[25]):
                    time_stamp = row[0]
                    subject_pos = row[1] + "," + row[2] + "," + row[3]
                    subject_rot = row[7] + "," + row[8] + "," + row[9]

                    id_25 = int(row[25].split("_")[1])

                    target_npc_name_index = 0
                    for item in row:
                        if "NPC" in str(item):
                            if str(id_25) in str(item):
                                target_npc_name_index = row.index(item)

                    if target_npc_name_index != 0:
                        npc_pos = row[target_npc_name_index + 1] + "," + row[target_npc_name_index + 2] + "," + row[target_npc_name_index + 3]
                        new_line = time_stamp + "," + subject_pos + "," + subject_rot + "," + npc_pos
                        gaze_info_lines.append(new_line)
                    else:
                        print("\nError! NPC Pos Info Not Locate Correctly.")
                        print("Current Level:" + str(level_name) + " Time:" + time_stamp + " NPC Name Ref:" + str(row[25]))
                        # os.system("pause")

    output_folder = get_parent_folder_path() + os.sep + "GroupData_Gaze_On_NPC_Full_Info"
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    output_path = output_folder + os.sep + str(level_name) + ".csv"
    header = "TimeStamp,SubjectPosX,SubjectPosY,SubjectPosZ,SubjectRotX,SubjectRotY,SubjectRotZ,NPC_PX,NPC_PY,NPC_PZ"
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
        progress_bar.set_description(f"提取受试者对NPC的注视")

if __name__ == "__main__":
    analyze()
