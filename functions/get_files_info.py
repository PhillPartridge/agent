import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        workingDirectoryAbs = os.path.abspath(working_directory)
        targetDirectory = os.path.normpath(os.path.join(workingDirectoryAbs, directory))
        commonpath = os.path.commonpath([workingDirectoryAbs, targetDirectory])

        if commonpath != workingDirectoryAbs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(targetDirectory):
            return f"Error: {directory} is not a directory"

        contentsOfDirectory = []
        contentsInDirectory = os.listdir(targetDirectory)
        for content in contentsInDirectory:
            fullPathContent = os.path.join(targetDirectory, content)
            contentsOfDirectory.append(
                f"- {content}: file_size={os.path.getsize(fullPathContent)} bytes, is_dir={os.path.isdir(fullPathContent)}"
            )
        joinedcontents = "\n".join(contentsOfDirectory)
        return (
            f"Result for {get_directory_label(directory)} directory:\n{joinedcontents}"
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
