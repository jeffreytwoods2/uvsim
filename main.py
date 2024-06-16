from classes import VM, ProgramLoader
import os

def get_file_path():
    file_path = input("Please provide a file to run:\n> ")

    while not os.path.exists(file_path):
        file_path = input("File not found. Please provide a valid file path:\n> ")
    
    return file_path

def main():
    file_path = get_file_path()
    vm = VM()
    pl = ProgramLoader()
    pl.load(vm, file_path)
    vm.run()

main()