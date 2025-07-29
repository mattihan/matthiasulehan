import os
from config import WORKING_DIRECTORY
from security import is_permitted_path
from google.genai import types


@is_permitted_path("write")
def write_file(file_path, contents):
    file_path = os.path.join(os.path.abspath(WORKING_DIRECTORY), file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(contents)
        return (
            f'Successfully wrote to "{file_path}" ({len(contents)} characters written)'
        )


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file specified by the file_path argument with the content specified by the contents argument.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path relative to the working directory to write the file to.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="The contents that should be written to the file",
            ),
        },
    ),
)
