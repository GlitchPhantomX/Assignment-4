import os

def rename_files(folder_path, prefix):
    for count, filename in enumerate(os.listdir(folder_path)):
        if os.path.isfile(os.path.join(folder_path, filename)):
            new_name = f"{prefix}_{count + 1}_{filename}"
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))

folder_path = input("Enter the folder path: ")
prefix = input("Enter the prefix for the files: ")
rename_files(folder_path, prefix)
