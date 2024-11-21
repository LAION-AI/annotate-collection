import json
import os
import math

# Create splits directory if it doesn't exist
splits_dir = "splits"
os.makedirs(splits_dir, exist_ok=True)

# Read the metadata file
with open("dataset_metadata.json", "r") as f:
    metadata = json.load(f)

# Calculate number of splits needed (2000 rows per split)
rows_per_split = 2000
total_splits = math.ceil(len(metadata) / rows_per_split)

# Split the data and write to files
for i in range(total_splits):
    start_idx = i * rows_per_split
    end_idx = min((i + 1) * rows_per_split, len(metadata))
    
    # Get data for this split
    split_data = metadata[start_idx:end_idx]
    
    # Extract only the required fields from each record
    filtered_data = []
    for idx, record in enumerate(split_data, start=start_idx):
        filtered_record = {
            'id': idx,
            'src': record['row']['image']['src'],
            'emotion': record['row']['Emotion'],
        }
        filtered_data.append(filtered_record)
    
    # Create filename with zero-padding (e.g., binary-00, binary-01)
    filename = f"binary-{str(i).zfill(2)}.json"
    filepath = os.path.join(splits_dir, filename)
    
    # Write filtered data to file
    with open(filepath, "w") as f:
        json.dump(filtered_data, f, indent=4)
    
    print(f"Created {filepath} with {len(filtered_data)} rows")
