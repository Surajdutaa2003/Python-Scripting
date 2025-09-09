import pytesseract
from PIL import Image
import json
import os

def extract_text_from_image(image_path, output_path="extracted_text.txt"):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)  # No hardcoded path needed
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        checkpoint = {
            "original_image": image_path,
            "extracted_text_length": len(text),
            "output_file": output_path
        }
        with open("text_extraction_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"Text extracted to {output_path}. Checkpoint saved.")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    image_file = input("Enter image path: ")
    if os.path.exists(image_file):
        extract_text_from_image(image_file)
    else:
        print("Image file not found!")
