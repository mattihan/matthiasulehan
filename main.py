import logging
import os
import sys
from config import SYSTEM_PROMPT, MAX_ITERATIONS
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions


class _NoToolNoise(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.getMessage().strip().startswith("Warning") == False


logging.getLogger("google_genai.types").addFilter(_NoToolNoise())


def add_verbose(func):
    def verbosify(response, verbose):
        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        return func(response, verbose)

    return verbosify


@add_verbose
def handle_function_calls(response, verbose):
    new_messages = []
    for call in response.function_calls:
        result = call_function(call, verbose)
        if not result.parts or not result.parts[0].function_response.response:
            raise SystemError(
                "There was no response from call_function or it is malformed"
            )
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        new_messages.append(result.parts[0])
    return types.Content(role="tool", parts=new_messages)


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT, tools=[available_functions]
        ),
    )

    return response


def query_bot(client, messages, verbose, limit=0):
    limit += 1
    if limit > MAX_ITERATIONS:
        print("Error: Maximum interations reached:", MAX_ITERATIONS)
        sys.exit(1)
    response = generate_content(client, messages)
    new_messages = messages.copy()
    if response.candidates:
        for candidate in response.candidates:
            new_messages.append(candidate.content)
    if not response.function_calls:
        return response.text
    else:
        print(response.text)
    new_messages.append(handle_function_calls(response, verbose))
    return query_bot(
        client,
        new_messages,
        verbose,
        limit,
    )


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    verbose_flag = False
    user_prompts = []

    for arg in sys.argv[1:]:
        match arg:
            case "--verbose":
                print("Setting verbose_flag=True")
                verbose_flag = True
                continue

            case _:
                user_prompts.append(arg)
    if verbose_flag:
        print(f"User prompt: {" ".join(user_prompts)}")
    initial_messages = [
        types.Content(role="user", parts=[types.Part(text=" ".join(user_prompts))])
    ]

    try:
        response = query_bot(client, initial_messages, verbose_flag)
        print(response)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    if not sys.argv or len(sys.argv) < 2:
        print("Usage: python3 main.py [options] <query_text>")
        print(
            """Options:
        --verbose # Include debugging information"""
        )
        sys.exit(1)

    main()
