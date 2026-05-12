import os
import shutil
folder_names = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']
current_dir = os.getcwd()
for folder_name in folder_names:
    folder_path = os.path.join(current_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
files = os.listdir(current_dir)
for file in files:
    file_path = os.path.join(current_dir, file)
    if os.path.isfile(file_path):
        prefix = file[:2]
        if prefix in folder_names:
            destination_folder = os.path.join(current_dir, prefix)
            shutil.move(file_path, os.path.join(destination_folder, file))
file_count = {}
for folder_name in folder_names:
    folder_path = os.path.join(current_dir, folder_name)
    file_count[folder_name] = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
sum_file_path = os.path.join(current_dir, 'Sum.txt')
with open(sum_file_path, 'w', encoding='utf-8') as f:
    for folder_name, count in file_count.items():
        f.write(f'{folder_name}: {count} 个文件\n')
print("操作完成！")
