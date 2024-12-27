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

# Keep image files that have a corresponding .txt file already
image_files = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.txt')]

print(f"Generating JSON for {len(image_files)} images...")
json_data = []
problematic_files = []

for image_file in image_files:
    # Extract the filename without extension and add .txt extension
    text_file_path = os.path.splitext(image_file)[0] + '.txt'

    rel_text_file_path = os.path.join(os.path.basename(os.path.dirname(text_file_path)), os.path.basename(text_file_path))
    # print(rel_text_file_path)
    rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

    description = ""
    try:
        with open(text_file_path, 'r', encoding='utf-8') as file:
            description = file.read()
    except UnicodeDecodeError:
        print(f"Could not decode file: {text_file_path}")
        problematic_files.append(text_file_path)

    json_data.append({
        "asset_path": rel_image_file_path,
        "description": description
    })

    print(".", end="")

print("")
# Write the JSON data to a file
json_file_path = "assets_index.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

print(f"JSON file generated at {json_file_path}")

# Write the list of problematic files to a file
problematic_files_path = 'problematic_files.txt'
with open(problematic_files_path, 'w') as file:
    for f in problematic_files:
        file.write(f + '\n')

print(f"List of problematic files written to {problematic_files_path}")
