import pandas as pd
import base64
import json
import os

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

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Process in batches of 2000
batch_size = 2000
num_parts = len(df) // batch_size

for part in range(num_parts):
    part_dir = f'./data/part-{part:02d}'
    ensure_dir(part_dir)
    
    start_idx = part * batch_size
    end_idx = start_idx + batch_size
    batch_df = df[start_idx:end_idx]
    
    for idx, row in enumerate(batch_df.iterrows()):
        row_dict = row[1].to_dict()
        # Encode image bytes to base64
        if 'image' in row_dict and 'bytes' in row_dict['image']:
            row_dict['image']['bytes'] = base64.b64encode(row_dict['image']['bytes']).decode('utf-8')
        row_json = json.dumps(row_dict)
        
        # Save to file with proper numbering
        filename = f'{idx:04d}.json'
        with open(os.path.join(part_dir, filename), 'w') as f:
            f.write(row_json)
    break