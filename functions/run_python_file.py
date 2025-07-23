import security
import os
import subprocess


@security.is_permitted_path("execute")
@security.exists
@security.is_python_file
def run_python_file(working_directory, file_path, args=[]):
    absolute_path = os.path.join(os.path.abspath(working_directory), file_path)
    try:
        completed = subprocess.run(
            ["python", absolute_path, *args],
            timeout=30,
            capture_output=True,
            cwd=os.path.abspath(working_directory),
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
