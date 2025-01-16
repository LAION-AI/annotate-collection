import os
import json
import base64
import random
from pathlib import Path
from pydub import AudioSegment
from io import BytesIO

# Define possible emotions
EMOTIONS = ['happy', 'sad', 'excited', 'confused']
SAMPLES_PER_PARTITION = 200

# Create base data directory
base_dir = Path('./data')
base_dir.mkdir(exist_ok=True)

sample_count = 0

# Process each WAV file
for wav_file in Path('./raw').glob('*.wav'):
    # Calculate current partition
    partition_num = sample_count // SAMPLES_PER_PARTITION
    partition_dir = base_dir / f'part-{partition_num:02d}'
    partition_dir.mkdir(exist_ok=True)
    
    # Load audio file and convert to MP3
    audio = AudioSegment.from_wav(wav_file)
    
    # Export as MP3 to BytesIO object
    mp3_buffer = BytesIO()
    audio.export(mp3_buffer, format='mp3', parameters=['-q:a', '2'])
    
    # Get MP3 bytes and encode to base64
    mp3_bytes = base64.b64encode(mp3_buffer.getvalue()).decode('utf-8')
    
    # Create JSON data
    json_data = {
        'id': f"audio-{sample_count:04d}",
        'label': random.choice(EMOTIONS),
        'audioBytes': mp3_bytes
    }
    
    # Write JSON file
    json_path = partition_dir / f'audio-{sample_count:04d}.json'
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    
    sample_count += 1

print(f"Conversion completed! Created {(sample_count-1) // SAMPLES_PER_PARTITION + 1} partitions")
