import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(
            os.path.join(working_directory_abs, directory)
        )
        commonpath = os.path.commonpath([working_directory_abs, target_directory])

        if commonpath != working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f"Error: {directory} is not a directory"

        contents_of_directory = []
        contents_in_directory = os.listdir(target_directory)
        for content in contents_in_directory:
            full_path_content = os.path.join(target_directory, content)
            contents_of_directory.append(
                f"- {content}: file_size={os.path.getsize(full_path_content)} bytes, is_dir={os.path.isdir(full_path_content)}"
            )
        joined_contents = "\n".join(contents_of_directory)
        return (
            f"Result for {get_directory_label(directory)} directory:\n{joined_contents}"
        )

    except Exception as e:
        return f"Error: error occurred in get_files_info [{e}]"


def get_directory_label(directory):
    return "current" if directory == "." else f"'{directory}'"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
