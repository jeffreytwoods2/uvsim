from config import *

class VMError(Exception):
    """Base class for VM-related errors."""
    pass

class InvalidWordError(VMError):
    """Raised when an invalid word is encountered."""
    pass

class InvalidMemoryAddressError(VMError):
    """Raised when an invalid memory address is accessed."""
    pass

class InvalidOpcodeError(VMError):
    """Raised when an invalid opcode is encountered."""
    pass

class VM:
    def __init__(self):
        self.program_counter = 0
        self.accumulator = 0
        self.reset_memory()
        self.input_func = input
        self.output_func = print
        self.halted = False
    
    def set_io_functions(self, input_func, output_func):
        self.input_func = input_func
        self.output_func = output_func
    
    def reset_memory(self):
        self.memory = ["+" + ("0" * WORD_LENGTH)] * MEMORY_LENGTH

    def halt(self):
        self.halted = True

    def is_valid_word(self, word: str) -> bool:
        try:
            int_value = int(word)
            return -10**WORD_LENGTH < int_value < 10**WORD_LENGTH
        except ValueError:
            return False

    def accumulator_overflow(self):
        return abs(self.accumulator) >= 10**WORD_LENGTH
    
    def truncate_accumulator(self):
        adjusted_acc_string = str(abs(self.accumulator))[-WORD_LENGTH:]
        self.accumulator = int(adjusted_acc_string) if self.accumulator >= 0 else -int(adjusted_acc_string)

    def read_op(self, operand: int):
        while True:
            try:
                word = self.input_func(f'Please enter a {WORD_LENGTH} digit word:\n')
                if not self.is_valid_word(word):
                    raise InvalidWordError(ERR_INVALID_WORD.format(WORD_LENGTH, "9" * WORD_LENGTH, "9" * WORD_LENGTH))
                break
            except InvalidWordError as e:
                self.output_func(str(e))
            except EOFError:
                self.output_func("\nPlease enter input on the last line of the console. Try again.")

        self.memory[operand] = f"{int(word):+07d}"
    
    def write_op(self, operand: int):
        self.output_func(self.memory[operand] + '\n')
    
    def load_op(self, operand: int):
        self.accumulator = int(self.memory[operand])
    
    def store_op(self, operand: int):
        '''Store a word from the accumulator into a specific location in memory'''
        if self.accumulator < 0:
            self.memory[operand] = f"{str(self.accumulator).zfill(7)}"
        else:
            self.memory[operand] = f"+{str(self.accumulator).zfill(6)}"
    
    def add_op(self, operand: int):
        self.accumulator += int(self.memory[operand])
    
    def subtract_op(self, operand: int):
        self.accumulator -= int(self.memory[operand])
    
    def divide_op(self, operand: int):
        divisor = int(self.memory[operand])
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.accumulator = int(self.accumulator / divisor)
    
    def multiply_op(self, operand: int):
        self.accumulator *= int(self.memory[operand])
    
    def branch_op(self, addr: int):
        if addr < 0 or addr >= MEMORY_LENGTH:
            raise InvalidMemoryAddressError(ERR_INVALID_MEMORY_ADDRESS.format(addr))
        self.program_counter = addr
    
    def branchneg_op(self, addr: int):
        if addr < 0 or addr >= MEMORY_LENGTH:
            raise InvalidMemoryAddressError(ERR_INVALID_MEMORY_ADDRESS.format(addr))
        if self.accumulator < 0:
            self.program_counter = addr
    
    def branchzero_op(self, addr: int):
        if addr < 0 or addr >= MEMORY_LENGTH:
            raise InvalidMemoryAddressError(ERR_INVALID_MEMORY_ADDRESS.format(addr))
        if self.accumulator == 0:
            self.program_counter = addr
    
    def __str__(self):
        vm_info = ("~" * 50) + "\n"
        vm_info += f"Program Counter: {self.program_counter}\nAccumulator: {self.accumulator}\nMemory:"

        row_count = MEMORY_LENGTH // 5
        for i in range(row_count):
            contents = f"\n{i:03d}: {self.memory[i]}\t{i+row_count:03d}: {self.memory[i+row_count]}\t{i+(row_count * 2):03d}: {self.memory[i+(row_count * 2)]}\t{i+(row_count * 3):03d}: {self.memory[i+(row_count * 3)]}\t{i+(row_count * 4):03d}: {self.memory[i+row_count * 4]}"
            vm_info += contents
        return vm_info

    def get_opcode(self, index) -> str:
        code = self.memory[index]
        return code[1:4]
    
    def process_next_step(self):
        code = self.memory[self.program_counter]
        opcode: str = self.get_opcode(self.program_counter)
        operand: int = int(code[4:7])

        if operand >= MEMORY_LENGTH:
            raise InvalidMemoryAddressError(ERR_INVALID_MEMORY_ADDRESS.format(operand))

        self.program_counter += 1

        operation = {
            "010": self.read_op,
            "011": self.write_op,
            "020": self.load_op,
            "021": self.store_op,
            "030": self.add_op,
            "031": self.subtract_op,
            "032": self.divide_op,
            "033": self.multiply_op,
            "040": self.branch_op,
            "041": self.branchneg_op,
            "042": self.branchzero_op,
            "043": lambda x: None  # HALT operation
        }.get(opcode)

        if operation is None:
            raise InvalidOpcodeError(ERR_INVALID_OPCODE.format(opcode))
        
        operation(operand)

        if self.accumulator_overflow():
            self.truncate_accumulator()

    def run(self):
        self.halted = False
        while not self.halted and self.get_opcode(self.program_counter) != "043":
            self.process_next_step()
        self.output_func("HALT.")
        self.program_counter += 1
    
    def run_by_step(self):
        while self.get_opcode(self.program_counter) != "043":
            self.process_next_step()
            yield
        self.output_func("HALT.")
        self.program_counter += 1
        
class ProgramLoader():
    old_word_length = 5
    old_op_codes = ("10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43")
    
    old_word_length = 5
    old_op_codes = ("10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43")
    
    @staticmethod
    def validate_code_format(code: str) -> str:
        if len(code) != 7 or code[0] not in ('+', '-') or not code[1:].isdigit():
            raise InvalidWordError(f"Invalid instruction: {code}")
        
    def convert_four_to_six(self, code: str) -> str:
        '''Convert a 4-length word to 6-length'''
        new_code = code

        if code[1:3] in self.old_op_codes:
            new_code = f"{code[0]}0{code[1:3]}0{code[3:]}"
        else:
            new_code = f"{code[0]}00{code[1:]}"
        
        return new_code
        
    def convert_four_to_six(self, code: str) -> str:
        '''Convert a 4-length word to 6-length'''
        new_code = code

        if code[1:3] in self.old_op_codes:
            new_code = f"{code[0]}0{code[1:3]}0{code[3:]}"
        else:
            new_code = f"{code[0]}00{code[1:]}"
        
        return new_code

    def load(self, vm: VM, filepath: str):
        user_program = ["+" + ("0" * WORD_LENGTH)] * MEMORY_LENGTH
        has_halt = False
        with open(filepath, "r") as f:
            lines = f.readlines()
            if len(lines) > MEMORY_LENGTH:
                raise MemoryError(ERR_PROGRAM_TOO_LARGE)
            
            for i in range(len(lines)):
                code = lines[i].strip()
                if len(code) == self.old_word_length:
                    code = self.convert_four_to_six(code)

                self.validate_code_format(code)
                
                if code[1:4] == "043":
                    has_halt = True
                
                user_program[i] = code

        if not has_halt:
            raise VMError(ERR_NO_HALT_INSTRUCTION)
        
        vm.memory = user_program

    def load_string(self, vm: VM, program: str):
        words = [line.strip() for line in program.split("\n")]
        if len(words) > MEMORY_LENGTH:
            raise MemoryError(ERR_PROGRAM_TOO_LARGE)

        vm.reset_memory()
        for i, code in enumerate(words):
            if not code:
                continue
            if len(code) == self.old_word_length:
                code = self.convert_four_to_six(code)
            self.validate_code_format(code)
            if len(code) == self.old_word_length:
                code = self.convert_four_to_six(code)
            vm.memory[i] = code
    
    def force_load(self, filepath: str, object):
        object.memory = []
        with open(filepath, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            code = line.strip()
            if len(code) == self.old_word_length:
                code = self.convert_four_to_six(code)
            if len(code) == self.old_word_length:
                code = self.convert_four_to_six(code)
            object.memory.append(code)

if __name__ == "__main__":
    vm = VM()
    pl = ProgramLoader()
    pl.load(vm, "test_files/6-digit-test.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)