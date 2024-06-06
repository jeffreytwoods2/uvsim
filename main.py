from vm import VM
import os
import sys

def get_file_path():
    # If there is no command line argument, default file will be used
    default_file = "test_files/Test1.txt"
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    else:
        print(f"No input file was given in the command line. Defaulting to {default_file}.")
        file_path = default_file

    if not os.path.exists(file_path):
        raise ValueError(f"File path {file_path} was not found.")
    
    return file_path

def main():
    file_path = get_file_path()
    vm = VM()
    vm.load_program(file_path)
    vm.run()
    print("\nFINAL STATE")
    print(vm)

main()
