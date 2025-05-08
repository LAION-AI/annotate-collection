import os
import shutil
import glob

def organize_json_files(root_dir):
    pattern = os.path.join(root_dir, '**', '*.json')
    json_files = glob.glob(pattern, recursive=True)
    for json_file in json_files:
        # Skip files already in with_aha_moment or without_aha_moment folders
        if any(folder in json_file for folder in ('/with_aha_moment/', '/without_aha_moment/')):
            continue
        parent_dir = os.path.dirname(json_file)
        with_aha_path = os.path.join(parent_dir, 'with_aha_moment')
        if not os.path.exists(with_aha_path):
            os.makedirs(with_aha_path)
        dst = os.path.join(with_aha_path, os.path.basename(json_file))
        shutil.move(json_file, dst)

if __name__ == "__main__":
    annotations_dir = os.path.join(os.path.dirname(__file__), "annotations")
    organize_json_files(annotations_dir)
