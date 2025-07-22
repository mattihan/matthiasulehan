import os


def is_permitted_path(func):
    def wrapper(*args, **kwargs):
        working_directory, file_path = args[:2]
        absolute_path = os.path.join(working_directory, file_path)
        if not os.path.abspath(absolute_path).startswith(
            os.path.abspath(working_directory)
        ):
            raise PermissionError(
                f'Cannot list "{file_path}" because it is outside the permitted working directory'
            )
        return func(*args, **kwargs)

    return wrapper


def is_dir(func):
    def wrapper(*args, **kwargs):
        working_directory, file_path = args[:2]
        absolute_path = os.path.join(working_directory, file_path)
        if not os.path.isdir(absolute_path):
            raise PermissionError(f'"{file_path}" is not a directory')
        return func(*args, **kwargs)

    return wrapper


def is_file(func):
    def wrapper(*args, **kwargs):
        working_directory, file_path = args[:2]
        absolute_path = os.path.join(working_directory, file_path)

        if not os.path.isfile(absolute_path):
            raise PermissionError(f'"{file_path}" is not a file')
        return func(*args, **kwargs)

    return wrapper
