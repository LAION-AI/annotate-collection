import os
import shutil

def move_json_folder_contents_up(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if dirname == "JSON":
                json_folder = os.path.join(dirpath, dirname)
                parent_folder = dirpath
                # Move all files and folders from JSON to parent
                for item in os.listdir(json_folder):
                    src = os.path.join(json_folder, item)
                    dst = os.path.join(parent_folder, item)
                    if os.path.exists(dst):
                        # If destination exists, remove it first
                        if os.path.isdir(dst):
                            shutil.rmtree(dst)
                        else:
                            os.remove(dst)
                    shutil.move(src, dst)
                # Remove the now-empty JSON folder
                os.rmdir(json_folder)

if __name__ == "__main__":
    annotations_dir = os.path.join(os.path.dirname(__file__), "annotations")
    move_json_folder_contents_up(annotations_dir)
