import os

from config import TEXT_LIMIT


def get_file_contents(working_directory, file):
    file_path = os.path.join(working_directory, file)
    if not os.path.isfile(file_path):
        return f"Error: File not found or is not a regular file: {file_path}"
    if not os.path.abspath(file_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(file_path, encoding="utf-8") as contents:
            text = contents.read()
            if len(text) > TEXT_LIMIT:
                return f'{text[:1001]}\n[...File "{file_path}" truncated at {TEXT_LIMIT} characters]'
            return text

    except Exception as e:
        return f"Error: {e}"
