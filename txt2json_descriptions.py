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
image_files = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.txt')]


print(f"Generating JSONs from TXT for {len(image_files)} images...")

for image_file in image_files:
    # Extract the filename without extension and add .txt extension
    text_file_path = os.path.splitext(image_file)[0] + '.txt'
    json_file_path = os.path.splitext(image_file)[0] + '.json'
    rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

    description = ""
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            description = file.read()
    except UnicodeDecodeError:
        print(f"Could not decode file: {text_file_path}")

    creation_time = os.path.getctime(text_file_path)
    creation_date = datetime.datetime.fromtimestamp(creation_time)

    llama_description = ""
    claude3haiku_description = ""

    if creation_date < datetime.datetime(2024, 12, 27):
      llama_description = description
    else:
      claude3haiku_description = description

    json_data = {
        "image": rel_image_file_path,
        "llama3.2-vision:11b": llama_description,
        "claude-3-haiku-20240307": claude3haiku_description
    }

    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file)

    print(".", end="")


