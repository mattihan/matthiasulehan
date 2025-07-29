from config import WORKING_DIRECTORY
import security
import os
import subprocess
from google.genai import types


@security.is_permitted_path("execute")
@security.exists
@security.is_python_file
def run_python_file(file_path, args=[]):
    absolute_path = os.path.join(WORKING_DIRECTORY, file_path)
    try:
        completed = subprocess.run(
            ["python", absolute_path, *args],
            timeout=30,
            capture_output=True,
            cwd=os.path.abspath(WORKING_DIRECTORY),
            text=True,
        )
    except Exception as e:
        return f"Error: executing python file: {e}"
    formatted = []
    if completed.stdout:
        formatted.append(f"STDOUT:\n{completed.stdout}")
    if completed.stderr:
        formatted.append(f"STDERR:\n{completed.stderr}")
    if completed.returncode != 0:
        formatted.append(f"\nProcess exited with code {completed.returncode}")
    return "\n".join(formatted) if formatted else "No output produced"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file and returns the output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the python file",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the python file",
                ),
            ),
        },
        required=["file_path"],
    ),
)
