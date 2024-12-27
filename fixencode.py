import os
from bs4 import UnicodeDammit

def convert_encoding(file_path, src_encoding='iso-8859-2', dest_encoding='utf-8'):
  try:
    with open(file_path, 'r', encoding=src_encoding) as file:
      content = file.read()
    
    with open(file_path, 'w', encoding=dest_encoding) as file:
      file.write(content)
    
    print(f"Converted {file_path} from {src_encoding} to {dest_encoding}")
  except Exception as e:
    print(f"Failed to convert {file_path}: {e}")

def convert_encoding_dammit(file_path, dest_encoding='utf-8'):
  try:
    with open(file_path, 'rb') as file:
      content = file.read()
    
    dammit = UnicodeDammit(content, ["cp-1250", "iso-8859-2"])
    with open(file_path, 'w', encoding=dest_encoding) as file:
      file.write(dammit.unicode_markup)
    
    print(f"Converted {file_path} to {dest_encoding}")
  except Exception as e:
    print(f"Failed to convert {file_path}: {e}")


def main():
  problematic_files_path = 'problematic_files.txt'
  
  if not os.path.exists(problematic_files_path):
    print(f"{problematic_files_path} does not exist.")
    return
  
  with open(problematic_files_path, 'r') as file:
    file_paths = file.readlines()
  
  for file_path in file_paths:
    file_path = file_path.strip()
    if os.path.exists(file_path):
      convert_encoding_dammit(file_path)
    else:
      print(f"File {file_path} does not exist.")

if __name__ == "__main__":
  main()