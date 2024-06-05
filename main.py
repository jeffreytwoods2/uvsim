from vm import VM

def main():
    vm = VM()
    vm.load_program("test_files/Test2.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)

main()
