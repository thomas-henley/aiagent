# write_file.py

import os

def write_file(working_directory, file_path, content):
    full_wd_path = os.path.abspath(working_directory)
    full_path = os.path.join(full_wd_path, file_path)
    if not full_path.startswith(full_wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # if not os.path.isfile(full_path):
    #     os.makedirs(full_path)
    
    with open(full_path, "w") as f:
        written = f.write(content)
        return f'Successfully wrote to "{file_path}" ({written} characters written)'