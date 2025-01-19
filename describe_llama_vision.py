import base64
import json
import sys
import os
import glob
import ollama


if len(sys.argv) != 2:
    print("Usage: python main.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# Check if the image_path is a directory
if os.path.isdir(image_path):
    # Get list of all files with image extensions in all subdirectories
    # image_extensions = ('*.jpg', '*.jpeg', '*.gif', '*.png')
    image_extensions = ('*.jpg', '*.jpeg', '*.png')
    # image_extensions = ('*.gif')
    # image_extensions = ('*.gif', '*.png')
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_path, '**', ext), recursive=True))
else:
    image_files = [image_path]

# Remove image files that have a corresponding .txt file already
# image_files = [f for f in image_files if not os.path.exists(os.path.splitext(f)[0] + '.txt')]

print(f"Processing {len(image_files)} images...")

processed_count = 0
skipped_count = 0
for image_file in image_files:
    try:
        # Extract the filename without extension and add .txt extension
        # text_file_path = os.path.splitext(image_file)[0] + '.txt'
        json_file_path = os.path.splitext(image_file)[0] + '.json'

        # Save the response content to the text file
        # with open(text_file_path, 'w') as file:
        #    file.write(response['message']['content'])

        # Save the response content to the json file as well
        rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

        json_data = {}
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
        # json_data["claude-3-haiku-20240307"] = description
        if not json_data.get("image"):
            json_data["image"] = rel_image_file_path
        if not json_data.get("llama3.2-vision:11b"):
            print(f"Processing {image_file} with llama3.2-vision:11b...")
            response = ollama.chat(
                model='llama3.2-vision:11b',
                # model='llava:7b',
                messages=[{
                    'role': 'user',
                    'content': 'What is in this image?',
                    'images': [image_file]
                }]
            )
            description = response['message']['content']
            json_data["llama3.2-vision:11b"] = description
            processed_count += 1
            print(f"Description: {description}")
            print("=====================================")
        else:
            print(f"Skipping image {image_file} as it has already been processed with llama3.2-vision:11b")
            skipped_count += 1

        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
        # end JSON handling

        # count += 1
        # print(f"Processed {count}/{len(image_files)} images")
        # print(f"Response saved to {text_file_path}")
    except ollama._types.ResponseError as e:
        print(f"Error processing image {image_file}: {e}")
        continue

print(f"Processed {processed_count} images, skipped {skipped_count} images. Out of {len(image_files)} images.")
