# Instructions

1. Put all images in the `images` folder of the corresponding project
2. Update the instructions in the `guide.json` of the corresponding project
3. Run the script `finder.py` to find all the images that are not being used in the `guide.json`
4. Upload your changes to the repository

## Guide JSON

The `guide.json` file is a JSON file that contains all the information about the project. It contains the following fields:

- `images`: A list of all the images in the project
- `instructions`: A guide for the annotators
- `options`: A dictionary of the annotation options for the project:
  - `key`: the modality (e.g., slider, checkbox, buttons, etc.)
  - `dictionary`: A dictionary of the possible values for the categories
    - `key`: The name of the category
    - `value`: The values of the category (are getting expanded in the UI)
- `title`: The title of the project
- `description`: A brief description of the project
