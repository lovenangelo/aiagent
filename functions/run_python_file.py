import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        workdir_abs_path = os.path.abspath(working_directory)
        abs_path = os.path.abspath(full_path)

        if not ".py" in file_path:
            return f'Error: "{file_path}" is not a Python file.'
        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_path.startswith(workdir_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        cp = subprocess.run(["python3",  abs_path] + [], timeout=30, cwd=workdir_abs_path, capture_output=True)

        print(cp.stdout)

        if cp.stdout == None and cp.stderr == None:
            return "No output produced"

        stdout = f"STDOUT: {cp.stdout}"
        stderr = f"STDERR: {cp.stderr}"

        if cp.returncode != 0:
            return "Process exited with code X"

        return stdout + stderr

    except Exception as e:
        return f'Error: executing Python file: {e}'

