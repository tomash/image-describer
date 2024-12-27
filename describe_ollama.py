import ollama
import sys
import os
import glob

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

# Remove image files that have a corresponding .txt file already
image_files = [f for f in image_files if not os.path.exists(os.path.splitext(f)[0] + '.txt')]

print(f"Processing {len(image_files)} images...")

count = 0
for image_file in image_files:
    try:
        response = ollama.chat(
            model='llama3.2-vision:11b',
            messages=[{
                'role': 'user',
                'content': 'What is in this image?',
                'images': [image_file]
            }]
        )

        # Extract the filename without extension and add .txt extension
        text_file_path = os.path.splitext(image_file)[0] + '.txt'

        # Save the response content to the text file
        with open(text_file_path, 'w') as file:
            file.write(response['message']['content'])

        count += 1
        print(f"Processed {count}/{len(image_files)} images")
        print(f"Response saved to {text_file_path}")

        print(response['message']['content'])
    except ollama._types.ResponseError as e:
        print(f"Error processing image {image_file}: {e}")
        continue

