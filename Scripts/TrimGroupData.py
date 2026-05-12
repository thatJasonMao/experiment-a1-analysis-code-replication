import os

group_changchun = []

def build_group_ref():
    global group_changchun
    target_path = get_parent_folder_path() + os.sep + "受试者采集数据_长春"
    dirs = get_subfolders_os(target_path)
    for dir in dirs:
        items = dir.split("_")
        if len(items) > 1:
            group_changchun.append(items[1])
    print(f"长春受试者数量{len(group_changchun)}")
    print(group_changchun)

def get_subfolders_os(directory):
    subfolders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subfolders.append(item)
    return subfolders

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

def execute_trim_path():
    global group_changchun
    group_data_path = get_parent_folder_path() + os.sep + "GroupData"
    files = get_all_file_paths(group_data_path)
    print(f"共找到源数据文件数量：{len(files)}")
    for file in files:
        file_name = os.path.basename(file)
        file_name = file_name.replace(".csv", "")
        items = file_name.split("_")
        subject_name = items[0]
        # print(subject_name)
        if subject_name not in group_changchun:
            os.remove(file)
            print(f"非长春受试者 删除文件：{file}")

if __name__ == "__main__":
    build_group_ref()
    execute_trim_path()
