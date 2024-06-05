from vm import VM
import os

def get_file_path():
    print("Please enter the path to your input file:")
    file_path = input("> ")
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
