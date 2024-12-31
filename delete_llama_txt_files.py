import datetime
import sys
import os
import glob
import json

if len(sys.argv) != 2:
    print("Usage: python main.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# Check if the image_path is a directory
if os.path.isdir(image_path):
    # Get list of all files with image extensions in all subdirectories
    image_extensions = ('*.jpg', '*.jpeg', '*.gif', '*.png')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_path, '**', ext), recursive=True))
else:
    image_files = [image_path]

# Keep image files that have a corresponding .txt file
image_files = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.json')]


print(f"Cleaning up Llama-generated txt files for {len(image_files)} images...")
count = 0

for image_file in image_files:
    # Extract the filename without extension and add .txt extension
    text_file_path = os.path.splitext(image_file)[0] + '.txt'
    json_file_path = os.path.splitext(image_file)[0] + '.json'
    # rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

    json_data = {}
    if os.path.exists(json_file_path):
      with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    description = ""
    llama_description = json_data.get("llama3.2-vision:11b", "")

    if llama_description: # If the Llama description is present, delete txt file
        os.remove(text_file_path)
        print("D", end="")
        count += 1
    else:
        print(".", end="")      


print(f"\nDeleted {count} Llama-generated txt files.")
