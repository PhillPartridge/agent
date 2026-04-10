import os
import subprocess
from config import SUBPROCESS_TIMEOUT
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )
        commonpath = os.path.commonpath([working_directory_abs, target_file_path])
        is_python_extension = file_path.endswith(".py")

        if commonpath != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not is_python_extension:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            capture_output=True,
            cwd=working_directory_abs,
            timeout=SUBPROCESS_TIMEOUT,
            text=True,
        )

        return parse_result(completed_process)

    except Exception as e:
        return f"Error: error occurred in run_python_file [{e}]"


def parse_result(completed_process):
    stdout = completed_process.stdout
    stderr = completed_process.stderr
    if completed_process.returncode != 0:
        return f"Process exited with code {completed_process.returncode}"

    if not stdout and not stderr:
        return "No output produced"

    return f"STDOUT:{stdout}\nSTDERR:{stderr}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Safely executes a Python file in a sandboxed directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments for the script.",
                items=types.Schema(
                    type=types.Type.STRING, description="Individual argument string"
                ),
            ),
        },
    ),
)
