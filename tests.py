from functions.get_file_contents import get_file_contents
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def test():
    print("=========================================================")
    print("Testing run_python_file...")
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
    print("=========================================================")
    print("Testing get_files_info...")
    print(get_files_info("calculator", directory="."))
    print(get_files_info("calculator", "/home/"))
    print(get_files_info("calculator", ".."))
    print("=========================================================")
    print("Testing get_file_contents...")
    print(get_file_contents("calculator", "lorem.txt"))
    print(get_file_contents("calculator", "../main.py"))
    print(get_file_contents("calculator", "nonexistent.txt"))
    print("=========================================================")
    print("Testing write_file...")
    print(write_file("calculator", "test_write.txt", "hello"))
    print(write_file("calculator", "/tmp/test_write.txt", "world"))
    print(write_file("calculator", "../test_write.txt", "foobar"))
    print("=========================================================")
    print("Tests concluded")


if __name__ == "__main__":
    test()
