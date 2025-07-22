import os
from security import is_permitted_path, is_dir


@is_permitted_path
@is_dir
def get_files_info(working_directory, directory="."):
    absolute_path = os.path.join(working_directory, directory)
    if not os.path.abspath(absolute_path).startswith(
        os.path.abspath(working_directory)
    ):
        return f'Error: Cannot list "{directory}" because it is outside the permitted working directory'
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    try:
        files = []
        for file in os.listdir(absolute_path):
            file_path = os.path.join(absolute_path, file)
            files.append(
                f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
            )
        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"
