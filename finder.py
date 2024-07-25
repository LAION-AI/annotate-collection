import os
import json
import random

# [
#     {
#         "title": "Facial Stance Detection",
#         "folder": "stance-detection-part-5",
#         "description": "Here you get to annotate images for facial emotion detection from a diverse set of images."
#     },
#     {
#         "title": "Test Annotation",
#         "folder": "stance-detection-part-2",
#         "description": "Testset for debugging purposes."
#     }
# ]

def update_projects_list(directory):
    # Get list of all directories in directory
    all_dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    # Open the projects.json file
    with open('./projects/projects.json', 'r') as f:
        # Load the JSON data
        data = json.load(f)
        
    new_data = []
        
    for d in all_dirs:
        # check if d is in any of the records folder 
        if not any(d == record['folder'] for record in data):
            # Add new record to data
            new_data.append({
                "title": d,
                "folder": d,
                "description": "Here you get to annotate images for facial emotion detection from a diverse set of images."
            })
        else:
            # update the description
            record = next((record for record in data if record['folder'] == d), None)
            new_data.append(record)
            
        ### sorted by title name
        new_data = sorted(new_data, key=lambda x: x['title'])
            
        with open('./projects/projects.json', "w") as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)
    

        # # Modify the JSON data to include the list of project directories
        # # data['projects'] = sorted(all_dirs)
        # for i in range(len(data)):
        #     data[i]['folder'] = all_dirs[i]

        # # Write the modified JSON data back to the file
        # file.seek(0)
        # json.dump(data, file, indent=4)
        # file.truncate()

def update_image_list(directory, randomize=False):
    # Get list of all files in directory
    all_files = os.listdir(os.path.join(directory, "images"))

    # Filter list to include only image files
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'))]

    # Open the guide.json file
    with open(os.path.join(directory, 'guide.json'), 'r+') as file:
        # Load the JSON data
        data = json.load(file)

        # Modify the "images" key
        if randomize == False:
            data['images'] = sorted(image_files)
        else:
            data['images'] = random.sample(image_files, len(image_files))

        # Write the modified JSON data back to the file
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
        
if __name__ == '__main__':
    update_projects_list('./projects')
    ### list only directorys in os.listdir()
    for p in sorted(os.listdir('./projects')):
        if p.endswith("7") or p.endswith("8"):
            if os.path.isdir(os.path.join('./projects', p)):
                print(f'./projects/{p}')
                update_image_list(f'./projects/{p}', randomize=True)