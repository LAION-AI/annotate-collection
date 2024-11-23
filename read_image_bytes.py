
from pathlib import Path

def print_image_bytes(image_path):
    # Read the image as bytes
    image_bytes = Path(image_path).read_bytes()
    # Print the bytes to console
    print(image_bytes)

if __name__ == "__main__":
    image_path = "/path/image.jpg"
    print_image_bytes(image_path)