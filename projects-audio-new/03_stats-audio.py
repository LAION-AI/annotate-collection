import json
import urllib.parse
from collections import defaultdict

INPUT_JSON = "cleaned-audio-files.json"

def extract_emotion_rating(url):
    """
    Extracts the emotion and rating from a URL.
    
    Expected URL structure:
      .../talent-emotion-bins/<Emotion>/<Rating>/<filename>.mp3
      
    Returns:
      (emotion, rating) as strings.
    """
    parts = url.rstrip('/').split('/')
    if len(parts) < 3:
        return None, None
    # Emotion is the third-to-last part; rating is the second-to-last.
    # URL decode the emotion category to handle %20 and other encoded characters
    emotion = urllib.parse.unquote(parts[-3])
    rating = parts[-2]
    return emotion, rating

def main():
    # Load the list of URLs from the cleaned JSON file.
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        urls = json.load(f)
    
    overall_count = len(urls)
    categories = set()
    
    # First, collect all ratings per emotion to determine their rating scheme
    emotion_ratings = defaultdict(set)
    emotion_urls = defaultdict(list)
    
    for url in urls:
        emotion, rating = extract_emotion_rating(url)
        if emotion is None or rating is None:
            continue
        
        categories.add(emotion)
        if rating.isdigit():
            emotion_ratings[emotion].add(int(rating))
            emotion_urls[emotion].append((url, rating))
    
    no_emotion_count = 0
    weak_emotion_count = 0
    strong_emotion_count = 0

    # Process URLs with rating statistics based on available ratings
    for emotion, urls_with_ratings in emotion_urls.items():
        available_ratings = emotion_ratings[emotion]

        print(f"Emotion: {emotion}, Number of ratings: {len(available_ratings)}")
        
        # Check if this emotion only has ratings 0, 1, and 2
        has_only_low_ratings = all(rating <= 2 for rating in available_ratings)
        
        for url, rating in urls_with_ratings:
            try:
                rating_int = int(rating)
                
                if has_only_low_ratings:
                    # Special case: If only 0,1,2 available
                    if rating_int == 0:
                        no_emotion_count += 1
                    elif rating_int == 1:
                        weak_emotion_count += 1
                    elif rating_int == 2:
                        strong_emotion_count += 1
                else:
                    # Standard case: 0 = no emotion, 1-2 = weak, >2 = strong
                    if rating_int == 0:
                        no_emotion_count += 1
                    elif rating_int <= 2:
                        weak_emotion_count += 1
                    else:
                        strong_emotion_count += 1
            except ValueError:
                # In case the rating is not an integer string
                pass

    print("Statistics:")
    print(categories)
    print(f"Overall count: {overall_count}")
    print(f"Number of categories: {len(categories)}")
    print(f"No-emotion (typically rating 0) count: {no_emotion_count}")
    print(f"Weak emotions count: {weak_emotion_count}")
    print(f"Strong emotions count: {strong_emotion_count}")
    
    # Print special case note
    print("\nNote: For emotions with only ratings 0-2, the ratings are interpreted as:")
    print("  0 = No emotion, 1 = Weak emotion, 2 = Strong emotion")
    print("For other emotions, ratings are interpreted as:")
    print("  0 = No emotion, 1-2 = Weak emotion, >2 = Strong emotion")

if __name__ == "__main__":
    main()
