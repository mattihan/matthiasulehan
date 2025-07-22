from functions.write_file import write_file

try:
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculartor", "/tmp/temp.txt", "this should not be allowed"))
except Exception as e:
    print(f"Error: {e}")
