import base64
import json
import sys
import os
import glob
import anthropic

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
image_files = [f for f in image_files if not os.path.exists(os.path.splitext(f)[0] + '.txt')]

print(f"Processing {len(image_files)} images...")

client = anthropic.Anthropic(
    api_key = os.environ['ANTHROPIC_API_KEY']
)

count = 0
for image_file in image_files:
    # Determine the media type based on the file extension
    media_type = None
    if image_file.lower().endswith(('.jpg', '.jpeg')):
        media_type = 'image/jpeg'
    elif image_file.lower().endswith('.png'):
        media_type = 'image/png'
    elif image_file.lower().endswith('.gif'):
        media_type = 'image/gif'
    else:
        print(f"Unsupported image format: {image_file}")
        continue

    image_base64 = base64.standard_b64encode(open(image_file, "rb").read()).decode("utf-8")

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Describe this image."
                        }
                    ],
                }
            ],
        )

        # Extract the filename without extension and add .txt extension
        text_file_path = os.path.splitext(image_file)[0] + '.txt'
        json_file_path = os.path.splitext(image_file)[0] + '.json'

        description = response.content[0].text

        # Save the response content to the text file
        with open(text_file_path, 'w') as file:
            file.write(description)
        # Save the response content to the json file as well
        rel_image_file_path = os.path.join(os.path.basename(os.path.dirname(image_file)), os.path.basename(image_file))

        json_data = {}
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
        json_data["claude-3-haiku-20240307"] = description
        if not json_data.get("image"):
            json_data["image"] = rel_image_file_path

        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
        # end JSON handling

        count += 1
        print(f"Processed {count}/{len(image_files)} images")
        print(f"Response saved to {text_file_path} and #{json_file_path}")

        print(description)
        print("=====================================")
    except anthropic.BadRequestError as e:
        print(f"Error processing image {image_file}: {e}")
        continue
    except anthropic.APIStatusError as e:
        print(f"Error processing image {image_file}: {e}")
        continue

