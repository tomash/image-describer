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
image_files_without_description = [f for f in image_files if not os.path.exists(os.path.splitext(f)[0] + '.txt')]
image_files_with_description = [f for f in image_files if os.path.exists(os.path.splitext(f)[0] + '.txt')]

print(f"Total: {len(image_files)} images...")
print(f"{len(image_files_with_description)} with description, {len(image_files_without_description)} without description")

