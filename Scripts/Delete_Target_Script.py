import os

target_script_name = "Record_Data_Modify.py"
target_folder_name_1 = "受试者采集数据_成都"
target_folder_name_2 = "受试者采集数据_深圳"
target_folder_name_3 = "受试者采集数据_长春"

upper_folder_path = os.path.abspath(__file__).replace("Scripts\Delete_Target_Script.py", "")
target_path_1 = upper_folder_path + target_folder_name_1
target_path_2 = upper_folder_path + target_folder_name_2
target_path_3 = upper_folder_path + target_folder_name_3

def delete_target_files(folder_path, target_name):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file == target_name:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"已删除文件: {file_path}")
                    except Exception as e:
                        print(f"删除文件 {file_path} 时出错: {e}")
    else:
        print(f"路径 {folder_path} 不存在或不是一个有效的目录。")

delete_target_files(target_path_1, target_script_name)
delete_target_files(target_path_2, target_script_name)
delete_target_files(target_path_3, target_script_name)
