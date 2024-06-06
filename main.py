from vm import VM
import os
import sys

def get_file_path():
    # Check for command line argument
    if len(sys.argv) < 2:
        return "test_files/Test1.txt" # If no command line argument, default to Test1.txt
    
    file_path = sys.argv[1]
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
