# get_files_info.py

import os

def get_files_info(working_directory, directory=None):
    # Get the working directory full path
    try:
        abs_working_dir = os.path.abspath(working_directory)
    except:
        return f"Error: Could not get abspath for {working_directory}"

    # Assign target_dir to working directory full path
    target_dir = abs_working_dir

    # If an optional directory was included, append it to the working dir
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    output = ""

    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            files_info.append(get_file_string(filepath))
        return "".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

# Output format:
# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False

def get_file_string(path):
    try:
        name = os.path.basename(path)
        file_size = os.path.getsize(path)
        is_dir = os.path.isdir(path)
    except:
        return f"Could not get metadata for {path}"
    
    return f"- {name}: file_size={file_size} bytes, is_dir={is_dir}\n"
