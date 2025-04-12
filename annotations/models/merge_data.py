import pandas as pd
import json
from pathlib import Path
import os # Keep os for path joining if preferred, but pathlib is generally cleaner

# --- Configuration ---
# 1. Specify the path to your base 'models' folder
models_folder_path = Path('.') # Or Path('/path/to/your/models/folder')

# --- Processing ---
all_data = [] # List to store data from all files

# Check if the base folder exists
if not models_folder_path.is_dir():
    print(f"Error: Base folder not found: {models_folder_path.resolve()}")
else:
    print(f"Scanning folder: {models_folder_path.resolve()}")
    # 3. Recursively find all .json files within the models folder
    #    We expect files under models/project/annotator/JSON/aha_status/image.json
    json_files = list(models_folder_path.rglob('*.json'))

    if not json_files:
        print(f"No .json files found recursively within {models_folder_path.resolve()}")
    else:
        print(f"Found {len(json_files)} .json files to process...")

        # 4. Loop through each found file
        for file_path in json_files:
            try:
                # 5. Extract information from the file path
                parts = file_path.parts

                # Determine the base index (0 if models_folder_path is '.', 1 otherwise)
                base_index = 0
                if models_folder_path.name == parts[0]:
                     base_index = 1
                elif str(models_folder_path.resolve()) != str(file_path.resolve().parent.parent.parent.parent.parent):
                    # Basic sanity check if the structure seems off, relative to a non-root models_folder_path
                     print(f"  Warning: Skipping file with unexpected path structure relative to base: {file_path}")
                     continue


                # Validate path length relative to the base folder path
                # Expected structure from base: project/annotator/JSON/aha_status/file.json
                # Needs at least 5 parts after the base
                expected_parts_count = base_index + 5
                if len(parts) < expected_parts_count:
                    print(f"  Warning: Skipping file with unexpected path depth: {file_path} (found {len(parts)} parts, expected at least {expected_parts_count})")
                    continue

                # Extract parts based on expected structure
                project_name = parts[base_index + 0]
                annotator_name = parts[base_index + 1]
                # parts[base_index + 2] should be 'JSON' - optionally check this
                aha_folder_name = parts[base_index + 3]
                image_filename_stem = file_path.stem # Filename without extension
                image_name_with_ext = f"{image_filename_stem}.png" # Add .png extension

                # 6. Determine aha_moment value
                aha_moment_value = -1 # Default invalid value
                if aha_folder_name == 'with_aha_moment':
                    aha_moment_value = 1
                elif aha_folder_name == 'without_aha_moment':
                    aha_moment_value = 0
                else:
                    print(f"  Warning: Skipping file with unrecognized aha_moment folder: '{aha_folder_name}' in path {file_path}")
                    continue # Skip this file if the folder name isn't recognized

                # 7. Read the JSON content
                with open(file_path, 'r', encoding='utf-8') as f:
                    value_data = json.load(f)
                    value_data = value_data.get('value', None) # Extract the 'value' key
                    # Convert the loaded JSON object (dict) to its string representation
                    # as shown in the desired output format. Use str() for literal representation.
                    value_string = str(value_data)

                # 8. Append extracted data as a dictionary to our list
                all_data.append({
                    'project': project_name,
                    'annotator': annotator_name,
                    'image': image_name_with_ext,
                    'value': value_string, # Store the string representation
                    'aha_moment': aha_moment_value
                })

            except json.JSONDecodeError:
                print(f"  Error: Could not decode JSON in file: {file_path}")
            except IndexError:
                 print(f"  Error: Path structure incorrect for file: {file_path}. Could not extract parts.")
            except Exception as e:
                 print(f"  Error: An unexpected error occurred processing file {file_path}: {e}")

    # 9. Create the Pandas DataFrame
    if all_data:
        df = pd.DataFrame(all_data)


        df.sort_values(by=['project', 'annotator'], inplace=True)

        # 10. Display the first few rows and info (optional)
        print("\n--- DataFrame Head ---")
        print(df.head())

        print("\n--- DataFrame Info ---")
        df.info()

        # Example: Check counts per annotator or project
        # print("\n--- Counts per Annotator ---")
        # print(df['annotator'].value_counts())

        # Example: Save to CSV
        df.to_csv("combined_model_annotations.csv", index=False)

    else:
        print("\nNo data was successfully processed to create a DataFrame.")