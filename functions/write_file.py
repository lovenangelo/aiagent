import os

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        workdir_abs_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        if not abs_path.startswith(workdir_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.exists(abs_path):
            with open(abs_path, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return f"Error: failed to write in {abs_path}"

    except Exception as e:
        return f"Error: {e}"

