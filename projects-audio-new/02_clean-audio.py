import json
import urllib.parse

INPUT_JSON = "filtered-audio-files.json"
OUTPUT_JSON = "cleaned-audio-files.json"

def extract_emotion(url):
    """
    Extracts the emotion category from the URL.
    Expected URL structure:
    .../talent-emotion-bins/<Emotion>/<Rating>/<filename>.mp3
    For example:
    http://.../Anger/3/00151d67_enhanced_1.mp3 will return 'Anger'
    """
    parts = url.rstrip('/').split('/')
    if len(parts) < 3:
        return None
    # URL decode the emotion category to handle %20 and other encoded characters
    return urllib.parse.unquote(parts[-3])

def main():
    # Load the list of URLs.
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        urls = json.load(f)

    forbidden_substrings = ["VocalBurst", "Recording", "vs.", "Age", "Gender", "Valence", "Background"]
    cleaned_urls = []

    # Filter out URLs whose emotion category contains a forbidden substring.
    for url in urls:
        emotion = extract_emotion(url)
        if emotion is None:
            continue
        if any(forbidden in emotion for forbidden in forbidden_substrings):
            continue
        cleaned_urls.append(url)
    
    # Save the cleaned list with ensure_ascii=False.
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cleaned_urls, f, indent=4, ensure_ascii=False)
    
    print(f"Cleaned list saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
