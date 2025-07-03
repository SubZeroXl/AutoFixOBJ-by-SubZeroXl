# AutoFixOBJ By SubZero

### 🔧 Automatically Fix Intraoral Scan OBJ Exports

This project is a background Python tool designed to help dental technicians and dentists automatically fix `.obj` files exported from intraoral scanners (IOS). It solves the common problem where OBJ coordinates use **commas (`,`)** instead of dots (`.`), making the files unreadable in MeshLab, Blender, or ExoCAD.

---

### 🧠 How It Works

1. Monitors a selected folder continuously.
2. Detects newly exported `.zip` files from IOS software.
3. Unzips the archive, finds `.obj` files, and replaces commas with dots.
4. Deletes the broken `.obj`, saves a new one with `_fixed_by_SubZero.obj`.
5. Repackages the folder as `originalname_fixed_by_SubZero.zip`
6. Keeps track of processed files using SHA-256 hashes so they are not reprocessed.

---

### 💡 Features

- Runs in the background
- No user interaction needed after initial folder selection
- Skips duplicates using a `hashes.json` file
- Works offline
- Written in Python 3.x

---

### ⚠️ Problem I'm Facing (Need Help!)

Even though I use SHA-256 hashing to track processed `.zip` files, the script still sometimes **reprocesses the same ZIP** multiple times or overwrites previous outputs.

If you're a Python dev and can help me debug this part, I’d greatly appreciate it 🙏

---

### 📥 Example Usage

```bash
python autofixobj.py
