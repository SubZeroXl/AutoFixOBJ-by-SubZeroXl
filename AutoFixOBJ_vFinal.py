import os
import zipfile
import shutil
import time
import json
import hashlib
import tkinter as tk
from tkinter import filedialog

# Step 1: Select export folder (only once)
root = tk.Tk()
root.withdraw()
watch_folder = filedialog.askdirectory(title="Sélectionnez le dossier d’exportation")

if not watch_folder:
    print("Aucun dossier sélectionné. Fermeture.")
    exit()

# Step 2: Load or create hashes.json
hashes_file = os.path.join(watch_folder, "hashes.json")
if os.path.exists(hashes_file):
    with open(hashes_file, "r") as f:
        processed_hashes = set(json.load(f))
else:
    processed_hashes = set()

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def fix_obj_files(folder_path):
    for root_dir, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".obj"):
                full_path = os.path.join(root_dir, filename)
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read().replace(",", ".")
                os.remove(full_path)
                with open(full_path.replace(".obj", "_fixed_by_Antar.obj"), "w", encoding="utf-8") as f:
                    f.write(content)

def repack_folder(folder_path, output_path):
    shutil.make_archive(output_path, 'zip', folder_path)

def process_zip(zip_path):
    name = os.path.splitext(os.path.basename(zip_path))[0]
    extract_path = os.path.join(watch_folder, name)
    shutil.unpack_archive(zip_path, extract_path)

    fix_obj_files(extract_path)

    # Remove bad original .obj files
    for root_dir, _, files in os.walk(extract_path):
        for f in files:
            if f.endswith(".obj") and not f.endswith("_fixed_by_Antar.obj"):
                os.remove(os.path.join(root_dir, f))

    output_zip = os.path.join(watch_folder, f"{name}_fixed_by_Antar")
    repack_folder(extract_path, output_zip)

    shutil.rmtree(extract_path)

def save_hashes():
    with open(hashes_file, "w") as f:
        json.dump(list(processed_hashes), f)

print(f"🟢 Watching folder: {watch_folder}")
while True:
    zip_files = [f for f in os.listdir(watch_folder) if f.endswith(".zip")]
    for zip_file in zip_files:
        full_path = os.path.join(watch_folder, zip_file)
        file_hash = calculate_hash(full_path)

        if file_hash in processed_hashes:
            continue

        print(f"🔧 New zip detected: {zip_file}")
        process_zip(full_path)
        processed_hashes.add(file_hash)
        save_hashes()
        print(f"✅ Done: {zip_file}")
    time.sleep(3)
