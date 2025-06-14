# run_python_file.py

import os
import subprocess

def run_python_file(working_directory, file_path):
    full_wd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(full_wd, file_path))
    if not full_path.startswith(full_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_proc = subprocess.run(['python3', file_path], cwd=full_wd, timeout=30, capture_output=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    output = ''
    output += f'STDOUT: {completed_proc.stdout}\n'
    output += f'STDERR: {completed_proc.stderr}\n'
    if completed_proc.returncode != 0:
        output += f'Process exited with code {completed_proc.returncode}'
    return output
