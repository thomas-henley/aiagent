# get_file_content.py
import os
from config import *

def get_file_content(working_directory, file_path):
    full_wd_path = os.path.abspath(working_directory)
    full_path = os.path.join(full_wd_path, file_path)
    print(f'full_path: {full_path}')

    if not full_path.startswith(full_wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'File not found or is not a regular file: "{file_path}'

    with open(full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string):
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string
