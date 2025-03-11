import json
import random
import urllib.parse

INPUT_JSON = "audio-files.json"
OUTPUT_JSON = "filtered-audio-files.json"

def extract_emotion_rating(url):
    """
    Extracts the emotion and rating from the URL.
    Expected URL structure:
    .../talent-emotion-bins/<Emotion>/<Rating>/<filename>.mp3
    For example:
    http://.../Anger/3/00151d67_enhanced_1.mp3
    will return ('Anger', '3')
    """
    parts = url.rstrip('/').split('/')
    if len(parts) < 3:
        return None, None
    # Emotion is the third last part; rating is the second last.
    emotion = urllib.parse.unquote(parts[-3])
    rating = parts[-2]
    return emotion, rating

def main():
    # Load the full list of URLs.
    with open(INPUT_JSON, "r") as f:
        urls = json.load(f)
    
    # Group the URLs by emotion and then rating.
    groups = {}
    for url in urls:
        emotion, rating = extract_emotion_rating(url)
        if emotion is None or rating is None:
            continue
        groups.setdefault(emotion, {}).setdefault(rating, []).append(url)
    
    sampled_urls = []
    
    # For each emotion and its ratings, sample the desired number.
    for emotion, rating_groups in groups.items():
        # Check if this emotion only has ratings 0, 1, and 2
        has_only_low_ratings = all(int(rating) <= 2 for rating in rating_groups.keys() if rating.isdigit())
        
        for rating, url_list in rating_groups.items():
            # Determine sample size based on the available ratings
            if has_only_low_ratings:
                # If only ratings 0, 1, 2 exist, select 100 for each
                sample_size = 100
            else:
                # Otherwise use the original logic (100 for rating "0", 50 for others)
                sample_size = 100 if rating == "0" else 50
                
            if len(url_list) > sample_size:
                selected = random.sample(url_list, sample_size)
            else:
                selected = url_list
                
            sampled_urls.extend(selected)
            print(f"Emotion: {emotion}, Rating: {rating} - selected {len(selected)} out of {len(url_list)} files.")
    
    # Save the resulting list to a JSON file.
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(sampled_urls, f, indent=4, ensure_ascii=False)
    
    print(f"\nFiltered list saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
