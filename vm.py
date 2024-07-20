class VM():
    memory_length = 250
    word_length = 6

    def __init__(self):
        self.program_counter = 0
        self.accumulator = 0
        self.reset_memory()
    
    def reset_memory(self):
        self.memory = ["+" + ("0" * self.word_length)] * self.memory_length

    def is_valid_word(self, word: str) -> bool:
        '''Check if a word is a valid four digit word'''
        try:
            int_value = int(word)
        except ValueError:
            return False
        
        return -9999 <= int_value <= 9999

    def accumulator_overflow(self):
        return self.accumulator > 9999 or self.accumulator < -9999
    
    def truncate_accumulator(self):
        adjusted_acc_string = str(self.accumulator)[-4:]
        if self.accumulator > 0:
            self.accumulator = int(adjusted_acc_string)
        else:
            self.accumulator = -int(adjusted_acc_string)

    def read_op(self, operand: int):
        '''Read a word from the keyboard into a specific location in memory'''
        try:
            word = input('Please enter a four digit word:\n')
            while not self.is_valid_word(word):
                word = input('Please enter a four digit word between -9999 and 9999:\n')
                
        except EOFError:
            print("\n" + "-" * 38)
            print("Please enter input on the last line of the console. Try again.")
            print("-" * 38, end="\n\n")
            self.read_op(operand)
            return

        if int(word) < 0:
            self.memory[operand] = f"{str(word).zfill(5)}"
        else:
            self.memory[operand] = f"+{str(word).zfill(4)}"
    
    def write_op(self, operand: int):
        '''Write a word from a specific location in memory to screen'''
        print(self.memory[operand])
    
    def load_op(self, operand: int):
        '''Load a word from a specific location in memory into the accumulator'''
        self.accumulator = int(self.memory[operand])
    
    def store_op(self, operand: int):
        '''Store a word from the accumulator into a specific location in memory'''
        if self.accumulator < 0:
            self.memory[operand] = f"{str(self.accumulator).zfill(5)}"
        else:
            self.memory[operand] = f"+{str(self.accumulator).zfill(4)}"
    
    def add_op(self, operand: int):
        '''Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)'''
        self.accumulator += int(self.memory[operand])
    
    def subtract_op(self, operand: int):
        '''Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)'''
        self.accumulator -= int(self.memory[operand])
    
    def divide_op(self, operand: int):
        '''Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator)'''
        self.accumulator = int(self.accumulator / int(self.memory[operand]))
    
    def multiply_op(self, operand: int):
        '''Multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)'''
        self.accumulator *= int(self.memory[operand])
    
    def branch_op(self, addr: int):
        '''Branch to a specific location in memory'''
        if addr < 0:
            print("Error: Invalid memory address. Program halted.")
            raise ValueError("Invalid memory address")
        self.program_counter = addr
    
    def branchneg_op(self, addr: int):
        '''Branch to a specific location in memory if the accumulator is negative'''
        if addr < 0:
            print("Error: Invalid memory address. Program halted.")
            raise ValueError("Invalid memory address")
        if self.accumulator < 0:
            self.program_counter = addr
    
    def branchzero_op(self, addr: int):
        '''Branch to a specific location in memory if the accumulator is zero'''
        if addr < 0:
            print("Error: Invalid memory address. Program halted.")
            raise ValueError("Invalid memory address")
        if self.accumulator == 0:
            self.program_counter = addr
    
    def __str__(self):
        vm_info = ("~" * 50) + "\n"
        vm_info += f"Program Counter: {self.program_counter}\nAccumulator: {self.accumulator}\nMemory:"

        row_count = self.memory_length // 5
        for i in range(row_count):
            contents = f"\n{i:03d}: {self.memory[i]}\t{i+row_count:03d}: {self.memory[i+row_count]}\t{i+(row_count * 2):03d}: {self.memory[i+(row_count * 2)]}\t{i+(row_count * 3):03d}: {self.memory[i+(row_count * 3)]}\t{i+(row_count * 4):03d}: {self.memory[i+row_count * 4]}"
            vm_info += contents
        return vm_info

    def get_opcode(self: str):
        code = self.memory[self.program_counter]
        opcode: str = code[1:3]
        return opcode
    
    def process_next_step(self):
        code = self.memory[self.program_counter]
        sign: str = code[0]
        opcode: str = self.get_opcode()
        operand: int = int(code[3:5])
        if sign == "-":
            operand *= -1

        self.program_counter += 1

        match opcode:
            case "10":
                self.read_op(operand)
            case "11":
                self.write_op(operand)
            case "20":
                self.load_op(operand)
            case "21":
                self.store_op(operand)
            case "30":
                self.add_op(operand)
            case "31":
                self.subtract_op(operand)
            case "32":
                self.divide_op(operand)
            case "33":
                self.multiply_op(operand)
            case "40":
                self.branch_op(operand)
            case "41":
                self.branchneg_op(operand)
            case "42":
                self.branchzero_op(operand)
            case "43":
                return
            case _:
                print(f"Error: invalid opcode: {opcode}. Program halted.")
                raise ValueError(f"Invalid opcode: {opcode}")
            
        if self.accumulator_overflow():
            self.truncate_accumulator()

    def run(self):
        while self.get_opcode() != "43":
            self.process_next_step()
        print("HALT.")
        self.program_counter += 1
    
    def run_by_step(self):
        while self.get_opcode() != "43":
            self.process_next_step()
            yield
        print("HALT.")
        self.program_counter += 1
        
class ProgramLoader():
    def validate_code_format(self, code: str):
        if len(code) != 5 or code[0] not in ('+', '-') or not code[1:].isdigit():
            raise ValueError(f"Invalid instruction: {code}")

    def load(self, vm: VM, filepath: str):
        '''Loads user program into memory if it passes all validity checks'''
        user_program = ["+" + ("0" * vm.word_length)] * vm.memory_length
        has_halt = False
        with open(filepath, "r") as f:
            lines = f.readlines()
            if len(lines) > vm.memory_length:
                raise MemoryError("Program larger than available memory")
            
            for i in range(len(lines)):
                code = lines[i].strip()
                self.validate_code_format(code)
                
                if code[1:3] == "43":
                    has_halt = True
                
                user_program[i] = code
        if has_halt:
            vm.memory = user_program
        else:
            print("Error: program does not contain HALT instruction. Program halted.")
            raise RuntimeError("Program does not contain HALT instruction")

    def load_string(self, vm: VM, program: str):
        '''Loads user program from a string'''
        words = [line.strip() for line in program.split("\n")]
        if len(words) > vm.memory_length:
            raise MemoryError("Program larger than available memory")

        vm.reset_memory()
        for i, code in enumerate(words):
            if not code:
                continue
            self.validate_code_format(code)
            vm.memory[i] = code
    
    def force_load(self, filepath: str, object):
        '''Loads program into memory without regardless of validity'''
        object.memory = []
        with open(filepath, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            code = line.strip()
            object.memory.append(code)

if __name__ == "__main__":
    vm = VM()
    pl = ProgramLoader()
    pl.load(vm, "test_files/Test3.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)
