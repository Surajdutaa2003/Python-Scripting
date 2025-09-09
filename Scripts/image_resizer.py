from PIL import Image
import json
import os

def resize_image_keep_ratio(image_path, output_path="resized_image.jpg", new_width=None, new_height=None):
    try:
        with Image.open(image_path) as img:
            original_width, original_height = img.size
            print(f"Original size: {original_width}x{original_height}")
            
            # Validate width and height
            if new_width is not None and new_width > original_width:
                print("Width too large! Must be smaller than original width.")
                return None
            if new_height is not None and new_height > original_height:
                print("Height too large! Must be smaller than original height.")
                return None
            
            # Calculate new size maintaining ratio
            if new_width is not None:
                ratio = new_width / original_width
                new_height = int(original_height * ratio)
            elif new_height is not None:
                ratio = new_height / original_height
                new_width = int(original_width * ratio)
            else:
                print("No valid width or height provided.")
                return None

            resized_img = img.resize((new_width, new_height))
            resized_img.save(output_path)
            
        # Checkpoint
        checkpoint = {"original_image": image_path, "original_size": (original_width, original_height),
                      "new_size": (new_width, new_height), "output_image": output_path}
        with open("image_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)
        
        print(f"Image resized to {new_width}x{new_height} -> {output_path}. Checkpoint saved.")
        return resized_img

    except Exception as e:
        print(f"Error: {e}")
        return None


# Usage
if __name__ == "__main__":
    image_file = input("Enter image path: ")
    if not os.path.exists(image_file):
        print("Image file not found!")
        exit()

    choice = input("Do you want to enter width or height? (w/h): ").lower()
    if choice == 'w':
        width = int(input("Enter desired width: "))
        resize_image_keep_ratio(image_file, new_width=width)
    elif choice == 'h':
        height = int(input("Enter desired height: "))
        resize_image_keep_ratio(image_file, new_height=height)
    else:
        print("Invalid choice!")
