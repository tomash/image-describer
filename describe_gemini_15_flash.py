import base64
import json
import sys
import os
import glob
import google.generativeai as genai
import PIL.Image
import time

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

print(f"Processing {len(image_files)} images...")


# image_path_1 = "path/to/your/image1.jpeg"  # Replace with the actual path to your first image
# image_path_2 = "path/to/your/image2.jpeg" # Replace with the actual path to your second image

# sample_file_1 = PIL.Image.open(image_path_1)
# sample_file_2 = PIL.Image.open(image_path_2)

#Choose a Gemini model.
model_id = "gemini-1.5-flash"
model = genai.GenerativeModel(model_name=model_id)

prompt = "Describe this image. OCR any text if present."

processed_count = 0
skipped_count = 0
requests_per_minute_limit = 15
requests_per_day_limit = 1500

start_time = time.time()
files_processed_since_reset = 0

for image_file in image_files:
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
    if not json_data.get("image"):
        json_data["image"] = rel_image_file_path
    if not json_data.get(model_id):
        print(f"Processing {image_file} with {model_id}...")
        sample_file_1 = PIL.Image.open(image_file)        
        response = model.generate_content([prompt, sample_file_1])
        description = response.text
        json_data[model_id] = description
        processed_count += 1
        files_processed_since_reset += 1

        print(f"Description: {description}")
        print("=====================================")
        
    else:
        print(f"Skipping image {image_file} as it has already been processed with {model_id}")
        skipped_count += 1

    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file)
    # end JSON handling

    # Check if the limit of 15 files per minute is reached
    if files_processed_since_reset >= requests_per_minute_limit:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            time_to_sleep = 60 - elapsed_time
            print(f"Sleeping for {time_to_sleep} seconds to respect rate limit...")
            time.sleep(time_to_sleep)
        # Reset the counter and start time
        files_processed_since_reset = 0
        start_time = time.time()

    if processed_count >= requests_per_day_limit:
        print(f"Processed {processed_count} images today. Exiting...")
        break


