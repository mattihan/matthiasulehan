import os
import sys
from config import SYSTEM_PROMPT
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_contents import schema_get_file_contents, get_file_contents
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file


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
        func(response, verbose=verbose_flag)

    return verbosify


@add_verbose
def print_response(response, verbose=False):
    if response.function_calls:
        for call in response.function_calls:
            response = call_function(call, verbose=verbose)
            if (
                not len(response.parts)
                or not response.parts[0].function_response.response
            ):
                raise Exception(
                    "There was no response from call_function or it is malformed"
                )
            elif verbose:
                print(f"-> {response.parts[0].function_response.response}")
    else:
        print(response.text)


func_dict = {
    "get_files_info": get_files_info,
    "get_file_contents": get_file_contents,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(func, verbose=False):
    call = (
        f" - Calling function: {func.name}"
        if not verbose
        else f"Calling function: {func.name}({func.args})"
    )
    print(call)

    if func.name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func.name, response={"error": f"Unknown function: {func.name}"}
                )
            ],
        )
    result = func_dict[func.name]("./calculator", **func.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func.name, response={"result": result}
            )
        ],
    )


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
