import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function

import config

verbose = False

def main():

    if len(sys.argv) < 2:
        print("Usage: python3 main.py [prompt]")
        exit(1)

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        global verbose
        verbose = True

    prompt = sys.argv[1]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    vprint(f"User prompt: {prompt}")

    generate_content(client, messages)


def get_function_declarations():
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Returns the text contents of a file in the working directory as a string.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path (relative to the working directory) to the file to retrieve the contents of. Required."
                )
            }
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a python file at the specified file path.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path, relative to the working directory, of the python script to execute. Required."
                )
            }
        )
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite a file at the specified file path with the provided content string.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path, relative to the working directory, of the file to write to. Required."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write into the file. Required.",
                )
            }
        )
    )

    function_declarations = [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]

    return function_declarations


def generate_content(client, messages):

    available_functions = types.Tool(
        function_declarations=get_function_declarations()
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=config.SYSTEM_PROMPT
        )
    )

    if response.function_calls:
        for call in response.function_calls:
            vprint(f"Calling function: {call.name}({call.args})")
            content = call_function(call, verbose=verbose)
            if content.parts[0].function_response.response:
                vprint(content.parts[0].function_response.response)
            else:
                raise Exception("Invalid response from GEMINI")

    else:
        print(response.text)

    vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    vprint(f"Response tokens: {response.usage_metadata.candidates_token_count}")



def vprint(msg):
    if verbose:
        print(msg)


main()