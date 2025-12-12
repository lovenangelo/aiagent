import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        workdir_abs_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)
        dirs = abs_path.split(full_path) 
        cd = dirs[-1]

        if not os.path.isdir(abs_path):
            return f'Error: "{directory}" is not a directory'
        if not abs_path.startswith(workdir_abs_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        contents = os.listdir(abs_path)
        contents = list(map(lambda c: f"- {c}: file_size={os.path.getsize(f"{full_path}/{c}")} bytes, is_dir={os.path.isfile(f"{full_path}/{c}")}" ,contents))

        result = f"Result for {cd}directory:\n" + '\n'.join(contents)

        return result
    except Exception as e:
        return f'Error: {e}'
