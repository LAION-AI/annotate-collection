import json
import base64
from pathlib import Path
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import time

# Get all JSON files from output directory
json_files = sorted(Path('./output').glob('*.json'))

for json_file in json_files:
    # Load JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Get audio data and metadata
    audio_bytes = base64.b64decode(data['audioBytes'])
    emotion = data['label']
    
    print(f"Playing {json_file.stem} - Emotion: {emotion}")
    
    # Convert bytes to audio and play
    audio = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
    play(audio)
    
    # Small pause between files
    time.sleep(1)

print("Playback completed!")
