import os
from security import is_permitted_path, is_file

from config import TEXT_LIMIT


@is_permitted_path
@is_file
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
