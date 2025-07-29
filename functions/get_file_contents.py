import os
import security
from google.genai import types
from config import TEXT_LIMIT, WORKING_DIRECTORY


@security.is_permitted_path("read")
@security.is_file
def get_file_contents(file_path):
    file_path = os.path.join(os.path.abspath(WORKING_DIRECTORY), file_path)
    try:
        with open(file_path, encoding="utf-8") as contents:
            text = contents.read()
            if len(text) > TEXT_LIMIT:
                return f'{text[:1001]}\n[...File "{file_path}" truncated at {TEXT_LIMIT} characters]'
            return text

    except Exception as e:
        return f"Error: {e}"


schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Reads the contents of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)
