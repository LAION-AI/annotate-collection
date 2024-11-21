import pandas as pd
import base64
import json
import os
from PIL import Image
import io

dfs = []
for i in range(5):
    df = pd.read_parquet(f'./raw/train-0000{i}-of-00005.parquet')
    dfs.append(df)
    
df = pd.concat(dfs)
    
print(len(df))
# 20000

print(df.head())
#                                          path  ...                                              image
# 0  /teamspace/studios/this_studio/flux2/0.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 1  /teamspace/studios/this_studio/flux2/1.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 2  /teamspace/studios/this_studio/flux2/2.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 3  /teamspace/studios/this_studio/flux2/3.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 4  /teamspace/studios/this_studio/flux2/4.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...

print(df.columns)
# Index(['path', 'ind', 'Prompt', 'Age', 'Ethnicity', 'Gender', 'Emotion',
#        'image'],
#       dtype='object')

# shuffle the dataframe
df = df.sample(frac=1).reset_index(drop=True)

# Move specific paths to end of DataFrame
last_paths = [
    '/teamspace/studios/this_studio/flux2/6903.jpg',
    '/teamspace/studios/this_studio/flux2/5341.jpg',
    '/teamspace/studios/this_studio/flux2/13450.jpg',
    '/teamspace/studios/this_studio/flux2/12844.jpg'
]

# Create mask for rows to move to end
mask = df['path'].isin(last_paths)
# Reorder DataFrame - non-matching rows first, then matching rows
df = pd.concat([df[~mask], df[mask]]).reset_index(drop=True)

print("This is the tail")
print(df.tail())

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Process in batches of 2000
batch_size = 2000
num_parts = len(df) // batch_size

# 0   /teamspace/studios/this_studio/flux2/8936.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 1  /teamspace/studios/this_studio/flux2/18537.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 2   /teamspace/studios/this_studio/flux2/3551.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...
# 3   /teamspace/studios/this_studio/flux2/5341.jpg  ...  {'bytes': b'<!DOCTYPE html>\n<!--[if lt IE 7]>...
# 4  /teamspace/studios/this_studio/flux2/10305.jpg  ...  {'bytes': b'\xff\xd8\xff\xe1\x00\xbcExif\x00\x...

def is_valid_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()  # Verify it's actually an image
        return True
    except:
        return False

for part in range(num_parts):
    part_dir = f'./data/part-{part:02d}'
    ensure_dir(part_dir)
    
    start_idx = part * batch_size
    end_idx = start_idx + batch_size
    batch_df = df[start_idx:end_idx]
    
    valid_idx = 0  # Keep track of valid images for filename numbering
    for _, row in enumerate(batch_df.iterrows()):
        row_dict = row[1].to_dict()
        
        # Check if image bytes are valid before processing
        if 'image' in row_dict and 'bytes' in row_dict['image']:
            # if not is_valid_image(row_dict['image']['bytes']):
            #     print(row_dict['path'], row_dict['ind'])
            #     continue  # Skip invalid images                
                
            row_dict['image']['bytes'] = base64.b64encode(row_dict['image']['bytes']).decode('utf-8')
            
            # Save valid images with sequential numbering
            filename = f'{valid_idx:04d}.json'
            with open(os.path.join(part_dir, filename), 'w') as f:
                f.write(json.dumps(row_dict))
            valid_idx += 1
    
    # if part == 0:  # Remove break if you want to process all parts
    #     break