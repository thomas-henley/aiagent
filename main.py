import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

def generate_content(client, messages):

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=config.SYSTEM_PROMPT)
        )

    print(response.text)

    vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    vprint(f"Response tokens: {response.usage_metadata.candidates_token_count}")



def vprint(msg):
    if verbose:
        print(msg)

main()