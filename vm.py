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
        '''Check if a word is a valid 6 digit word'''
        try:
            int_value = int(word)
        except ValueError:
            return False
        
        return -999999 <= int_value <= 999999

    def accumulator_overflow(self):
        return self.accumulator > 999999 or self.accumulator < -999999
    
    def truncate_accumulator(self):
        adjusted_acc_string = str(self.accumulator)[-6:]
        if self.accumulator > 0:
            self.accumulator = int(adjusted_acc_string)
        else:
            self.accumulator = -int(adjusted_acc_string)

    def read_op(self, operand: int):
        '''Read a word from the keyboard into a specific location in memory'''
        try:
            word = input(f'Please enter a {self.word_length} digit word:\n')
            while not self.is_valid_word(word):
                word = input(f'Please enter a {self.word_length} digit word between -{"9" * self.word_length} and {"9" * self.word_length}:\n')
                
        except EOFError:
            print("\n" + "-" * 38)
            print("Please enter input on the last line of the console. Try again.")
            print("-" * 38, end="\n\n")
            self.read_op(operand)
            return

        if int(word) < 0:
            self.memory[operand] = f"{str(word).zfill(self.word_length + 1)}"
        else:
            self.memory[operand] = f"+{str(word).zfill(self.word_length)}"
    
    def write_op(self, operand: int):
        '''Write a word from a specific location in memory to screen'''
        print(self.memory[operand])
    
    def load_op(self, operand: int):
        '''Load a word from a specific location in memory into the accumulator'''
        self.accumulator = int(self.memory[operand])
    
    def store_op(self, operand: int):
        '''Store a word from the accumulator into a specific location in memory'''
        if self.accumulator < 0:
            self.memory[operand] = f"{str(self.accumulator).zfill(7)}"
        else:
            self.memory[operand] = f"+{str(self.accumulator).zfill(6)}"
    
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

    def get_opcode(self, index) -> str:
        code = self.memory[index]
        opcode: str = code[1:4]
        return opcode
    
    def process_next_step(self):
        code = self.memory[self.program_counter]
        opcode: str = self.get_opcode(self.program_counter)
        operand: int = int(code[4:7])

        if operand > self.memory_length - 1:
            print(f"Error: Word in address {str(self.program_counter).zfill(3)} targets invalid memory address {operand}. Program halted.")
            raise ValueError(f"Invalid memory address: {operand}")

        self.program_counter += 1

        match opcode:
            case "010":
                self.read_op(operand)
            case "011":
                self.write_op(operand)
            case "020":
                self.load_op(operand)
            case "021":
                self.store_op(operand)
            case "030":
                self.add_op(operand)
            case "031":
                self.subtract_op(operand)
            case "032":
                self.divide_op(operand)
            case "033":
                self.multiply_op(operand)
            case "040":
                self.branch_op(operand)
            case "041":
                self.branchneg_op(operand)
            case "042":
                self.branchzero_op(operand)
            case "043":
                return
            case _:
                print(f"Error: invalid opcode: {opcode}. Program halted.")
                raise ValueError(f"Invalid opcode: {opcode}")
            
        if self.accumulator_overflow():
            self.truncate_accumulator()

    def run(self):
        while self.get_opcode(self.program_counter) != "043":
            self.process_next_step()
        print("HALT.")
        self.program_counter += 1
    
    def run_by_step(self):
        while self.get_opcode(self.program_counter) != "043":
            self.process_next_step()
            yield
        print("HALT.")
        self.program_counter += 1
        
class ProgramLoader():
    old_word_length = 5
    old_op_codes = ("10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43")
    
    def validate_code_format(self, code: str) -> str:
        if len(code) != 7 or code[0] not in ('+', '-') or not code[1:].isdigit():
            raise ValueError(f"Invalid instruction: {code}")
        
    def convert_old_to_new(self, code: str):
        new_code = code

        if code[1:3] in self.old_op_codes:
            new_code = f"{code[0]}0{code[1:3]}0{code[3:]}"
        else:
            new_code = f"{code[0]}00{code[1:]}"
        
        return new_code

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
                if len(code) == self.old_word_length:
                    code = self.convert_old_to_new(code)

                self.validate_code_format(code)
                
                if code[1:4] == "043":
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
            if len(code) == self.old_word_length:
                code = self.convert_old_to_new(code)
            vm.memory[i] = code
    
    def force_load(self, filepath: str, object):
        '''Loads program into memory without regardless of validity'''
        object.memory = []
        with open(filepath, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            code = line.strip()
            if len(code) == self.old_word_length:
                code = self.convert_old_to_new(code)
            object.memory.append(code)

if __name__ == "__main__":
    vm = VM()
    pl = ProgramLoader()
    pl.load(vm, "test_files/6-digit-test.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)
