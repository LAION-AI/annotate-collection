import os
import json

projects = ["p1", "ptest"]

def update_image_list(directory):
    # Get list of all files in directory
    all_files = os.listdir(os.path.join(directory, "images"))

    # Filter list to include only image files
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

    # Open the guide.json file
    with open(os.path.join(directory, 'guide.json'), 'r+') as file:
        # Load the JSON data
        data = json.load(file)

        # Modify the "images" key
        data['images'] = image_files

        # Write the modified JSON data back to the file
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        
if __name__ == '__main__':
    for p in projects:
        update_image_list(f'./projects/{p}')