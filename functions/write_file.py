import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        workingDirectoryAbs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(workingDirectoryAbs, file_path)
        )
        commonpath = os.path.commonpath([workingDirectoryAbs, target_file_path])

        if commonpath != workingDirectoryAbs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(workingDirectoryAbs, exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: error occurred in write_file [{e}]"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to specified file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to working_directory, whose contents will be read and returned.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content taken from another file",
            ),
        },
    ),
)
