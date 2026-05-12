import os

current_dir = os.getcwd()
folder_name = os.path.basename(current_dir)

for filename in os.listdir(current_dir):
    if filename.endswith('.csv') and os.path.isfile(os.path.join(current_dir, filename)):
        new_name = f"{folder_name}_{filename}"

        old_path = os.path.join(current_dir, filename)
        new_path = os.path.join(current_dir, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
