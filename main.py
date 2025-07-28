import os
import sys
from config import SYSTEM_PROMPT
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_contents import schema_get_file_contents
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
verbose_flag = False
user_prompts = []
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ]
)


def add_verbose(func):
    def verbosify(response):
        if verbose_flag:
            print(f"User prompt: {user_prompts}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        func(response)

    return verbosify


@add_verbose
def print_response(response):
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(response.text)


def main():
    messages = [
        types.Content(role="user", parts=[types.Part(text=" ".join(user_prompts))])
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, tools=[available_functions]
        ),
    )
    print_response(response)


if __name__ == "__main__":
    if not sys.argv or len(sys.argv) < 2:
        print("Usage: python3 main.py [options] <query_text>")
        print(
            """Options:
        --verbose # Include debugging information"""
        )
        sys.exit(1)

    for arg in sys.argv[1:]:
        match arg:
            case "--verbose":
                verbose_flag = True
                continue

            case _:
                user_prompts.append(arg)
    main()
