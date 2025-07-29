import os
from config import WORKING_DIRECTORY


class SecurityFunctionArgs:
    WORKING_DIRECTORY = 0
    FILE_PATH = 1
    ABSOLUTE_PATH = 2


def security_decorator_generator(
    rule,
    error=(
        lambda *args: f"Error: Permission denied for {args[SecurityFunctionArgs.FILE_PATH]} at {args[SecurityFunctionArgs.ABSOLUTE_PATH]}"
    ),
):
    def outer(func):
        def inner(*args, **kwargs):
            if len(args) > 1:
                file_path = args[1]
            elif "file_path" in kwargs:
                file_path = kwargs["file_path"]
            elif "directory" in kwargs:
                file_path = kwargs["directory"]
            else:
                file_path = "."
            absolute_path = os.path.abspath(os.path.join(WORKING_DIRECTORY, file_path))
            if not rule(WORKING_DIRECTORY, file_path, absolute_path):
                return error(WORKING_DIRECTORY, file_path, absolute_path)
            return func(*args, **kwargs)

        return inner

    return outer


exists = security_decorator_generator(
    lambda *args: os.path.exists(args[SecurityFunctionArgs.ABSOLUTE_PATH]),
    lambda *args: f'Error: File "{args[SecurityFunctionArgs.FILE_PATH]}" not found',
)
is_python_file = security_decorator_generator(
    lambda *args: args[SecurityFunctionArgs.FILE_PATH][-3:] == ".py",
    lambda *args: f'Error: "{args[1]} is not a Python file',
)


def is_permitted_path(action="list"):
    return security_decorator_generator(
        lambda *args: args[SecurityFunctionArgs.ABSOLUTE_PATH].startswith(
            os.path.abspath(args[SecurityFunctionArgs.WORKING_DIRECTORY])
        ),
        lambda *args: f'Error: Cannot {action} "{args[SecurityFunctionArgs.FILE_PATH]}" as it is outside the permitted working directory',
    )


is_dir = security_decorator_generator(
    lambda *args: os.path.isdir(args[SecurityFunctionArgs.ABSOLUTE_PATH]),
    lambda *args: f'Error: "{args[SecurityFunctionArgs.FILE_PATH]}" is not a directory',
)
is_file = security_decorator_generator(
    lambda *args: os.path.isfile(args[SecurityFunctionArgs.ABSOLUTE_PATH]),
    lambda *args: f'Error: "{args[SecurityFunctionArgs.FILE_PATH]}" is not a file',
)
