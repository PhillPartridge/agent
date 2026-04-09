import os

working_directory = "calculator"
directory = "/bin"
workingDirectoryAbs = os.path.abspath(working_directory)
targetDirectory = os.path.normpath(os.path.join(workingDirectoryAbs, directory))
commonpath = os.path.commonpath([workingDirectoryAbs, targetDirectory])

print(
    f"working_directory = {working_directory}, directory = {directory}, workingDirectoryAbs = {workingDirectoryAbs}, targetDirectory = {targetDirectory}, commmonpath = {commonpath}"
)
