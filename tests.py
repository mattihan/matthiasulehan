from functions.get_file_contents import get_file_contents

print(get_file_contents("calculator", "main.py"))
print(get_file_contents("calculator", "pkg/calculator.py"))
print(get_file_contents("calculator", "/bin/cat"))
print(get_file_contents("calculator", "pkg/does_not_exist.py"))
