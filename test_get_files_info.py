from functions.get_files_info import get_files_info

tests = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]


for test in tests:
    print(get_files_info(test[0], test[1]))
