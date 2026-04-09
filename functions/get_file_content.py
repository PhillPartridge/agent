import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        workingDirectoryAbs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(workingDirectoryAbs, file_path)
        )
        commonpath = os.path.commonpath([workingDirectoryAbs, target_file_path])

        if commonpath != workingDirectoryAbs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += (
                    f"[File '{file_path}' truncated at {MAX_CHARS} characters]"
                )
        return file_content
    except Exception as e:
        return f"Error: occurred in get_file_content [{e}]"


schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads a file in a specified directory relative to working directory, providing its contents at a maximum of {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to working_directory, whose contents will be read and returned.",
            ),
        },
    ),
)
