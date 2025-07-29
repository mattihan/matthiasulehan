from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_contents import schema_get_file_contents, get_file_contents
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
    ]
)
func_dict = {
    "get_files_info": get_files_info,
    "get_file_contents": get_file_contents,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(func, verbose):
    print(
        " - Calling function:",
        func.name if not verbose else f"{func.name}({func.args})",
    )

    if func.name not in func_dict:
        return get_function_response_content(
            name=func.name, response={"error": f"Unknown function: {func.name}"}
        )
    result = func_dict[func.name](**func.args)
    return get_function_response_content(name=func.name, response={"result": result})


def get_function_response_content(name, response):
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(name=name, response=response)],
    )
