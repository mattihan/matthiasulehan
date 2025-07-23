import os
import security
from google.genai import types
from config import TEXT_LIMIT


@security.is_permitted_path
@security.is_file
def get_file_contents(working_directory, file):
    file_path = os.path.join(working_directory, file)
    try:
        with open(file_path, encoding="utf-8") as contents:
            text = contents.read()
            if len(text) > TEXT_LIMIT:
                return f'{text[:1001]}\n[...File "{file_path}" truncated at {TEXT_LIMIT} characters]'
            return text

    except Exception as e:
        return f"Error: {e}"


schema_get_files_contents = types.FunctionDeclaration(
    name="get_files_contents",
    description="Reads the contents of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)
