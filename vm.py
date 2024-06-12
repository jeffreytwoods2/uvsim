class VM():
    def __init__(self):
        self.memory = ["+0000"] * 100
        self.program_counter = 0
        self.accumulator = 0
    
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
        word = input('Please enter a four digit word:\n> ')
        while int(word) > 9999 or int(word) < -9999:
            word = input('Please enter a four digit word between -9999 and 9999:\n> ')

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
            raise ValueError("Invalid memory address")
        self.program_counter = addr
    
    def branchneg_op(self, addr: int):
        '''Branch to a specific location in memory if the accumulator is negative'''
        if addr < 0:
            raise ValueError("Invalid memory address")
        if self.accumulator < 0:
            self.program_counter = addr
    
    def branchzero_op(self, addr: int):
        '''Branch to a specific location in memory if the accumulator is zero'''
        if addr < 0:
            raise ValueError("Invalid memory address")
        if self.accumulator == 0:
            self.program_counter = addr
    
    def __str__(self):
        print("~" * 50)
        vm_info = f"Program Counter: {self.program_counter}\nAccumulator: {self.accumulator}\nMemory:"
        for i in range(20):
            contents = f"\n{i:02d}: {self.memory[i]}\t{i+20:02d}: {self.memory[i+20]}\t{i+40:02d}: {self.memory[i+40]}\t{i+60:02d}: {self.memory[i+60]}\t{i+80:02d}: {self.memory[i+80]}"
            vm_info += contents
        return vm_info
    
    def load_program(self, filepath: str):
        with open(filepath, "r") as f:
            lines = f.readlines()
            if len(lines) > 100:
                raise MemoryError("Program larger than available memory")
            
            for i in range(len(lines)):
                code = lines[i].strip()
                if len(code) != 5 or code[0] not in ('+', '-') or not code[1:].isdigit():
                    raise ValueError(f"Invalid instruction: {code}")
                
                self.memory[i] = code

    def run(self):
        while True:
            code = self.memory[self.program_counter]
            sign: str = code[0]
            opcode: str = code[1:3]
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
                    raise ValueError(f"Invalid opcode: {opcode}")
            
            if self.accumulator_overflow():
                self.truncate_accumulator()

if __name__ == "__main__":
    vm = VM()
    vm.load_program("test_files/Test2.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)
