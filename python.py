import os
import time
import zipfile
import rarfile
import tkinter as tk
from tkinter import filedialog

def unzip_and_fix(folder):
    while True:
        for filename in os.listdir(folder):
            if filename.endswith('.zip') or filename.endswith('.rar'):
                file_path = os.path.join(folder, filename)
                if filename.endswith('.zip'):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(folder)
                elif filename.endswith('.rar'):
                    with rarfile.RarFile(file_path, 'r') as rar_ref:
                        rar_ref.extractall(folder)

                for root, dirs, files in os.walk(folder):
                    for file in files:
                        if file.endswith('.obj'):
                            obj_path = os.path.join(root, file)
                            with open(obj_path, 'r') as f:
                                content = f.read().replace(',', '.')
                            with open(obj_path, 'w') as f:
                                f.write(content)

                new_filename = filename.rsplit('.', 1)[0] + '_fixed_by_antar.' + filename.rsplit('.', 1)[1]
                new_file_path = os.path.join(folder, new_filename)
                if filename.endswith('.zip'):
                    with zipfile.ZipFile(new_file_path, 'w') as zip_ref:
                        for foldername, subfolders, files in os.walk(folder):
                            for file in files:
                                zip_ref.write(os.path.join(foldername, file), arcname=file)
                elif filename.endswith('.rar'):
                    with rarfile.RarFile(new_file_path, 'w') as rar_ref:
                        for foldername, subfolders, files in os.walk(folder):
                            for file in files:
                                rar_ref.write(os.path.join(foldername, file), arcname=file)

                os.remove(file_path)

        time.sleep(10)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    unzip_and_fix(folder_selected)

if __name__ == "__main__":
    select_folder()
