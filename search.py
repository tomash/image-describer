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
# image_files = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.txt')]

# Keep image files that have a corresponding .json file already
image_files = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.json')]


print(f"Generating JSON for {len(image_files)} images...")
json_data = []
problematic_files = []

for image_file in image_files:
    #rel_text_file_path = os.path.join(os.path.basename(os.path.dirname(text_file_path)), os.path.basename(text_file_path))
    # print(rel_text_file_path)
    rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

    # Extract the filename without extension and add .json extension
    image_json_file_path = os.path.splitext(image_file)[0] + '.json'
    image_json_data = {}
    if os.path.exists(image_json_file_path):
        with open(image_json_file_path, 'r') as image_json_file:
            image_json_data = json.load(image_json_file)

    description = ""
    if "claude-3-haiku-20240307" in image_json_data:
        description = description + "Claude-3-Haiku 20240707: " + image_json_data["claude-3-haiku-20240307"] + "\n"

    if "llama3.2-vision:11b" in image_json_data:
        description = description + "LLama 3.2-Vision:11b: " + image_json_data["llama3.2-vision:11b"] + "\n"

    if "gemini-1.5-flash" in image_json_data:
        description = description + "Gemini 1.5 Flash: " + image_json_data["gemini-1.5-flash"] + "\n"

    # Extract the filename without extension and add .txt extension
    # text_file_path = os.path.splitext(image_file)[0] + '.txt'
    # try:
    #     with open(text_file_path, 'r', encoding='utf-8') as file:
    #         description = file.read()
    # except UnicodeDecodeError:
    #     print(f"Could not decode file: {text_file_path}")
    #     problematic_files.append(text_file_path)

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
