import os
from security import is_permitted_path


@is_permitted_path
def write_file(working_directory, file_path, contents):
    file_path = os.path.join(working_directory, file_path)
    with open(file_path, "w") as file:
        file.write(contents)
        print(
            f'Successfully wrote to "{file_path}" ({len(contents)} characters written)'
        )
