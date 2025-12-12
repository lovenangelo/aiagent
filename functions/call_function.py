from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from google.genai import types

def call_function(fcp, verbose=False):

    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if fcp.name not in functions.keys():
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
            )
            ],
            )

    if verbose:
        print(f"Calling function: {fcp.name}({fcp.args})")
    else:
        print(f" - Calling function: {fcp.name}")

    run = functions[fcp.name]

    res = run("./calculator", **fcp.args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=fcp.name,
            response={"result": res},
        )
    ],
)

