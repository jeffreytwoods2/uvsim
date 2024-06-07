from vm import VM
import os

def get_file_path():
    file_path = input("Please provide a file to run:\n> ")

    while not os.path.exists(file_path):
        file_path = input("File not found. Please provide a valid file path:\n> ")
    
    return file_path

def main():
    file_path = get_file_path()
    vm = VM()
    vm.load_program(file_path)
    vm.run()

main()
