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
    
    def reset_memory(self):
        self.memory = ["+" + ("0" * WORD_LENGTH)] * MEMORY_LENGTH

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
                word = input(f'Please enter a {WORD_LENGTH} digit word:\n')
                if not self.is_valid_word(word):
                    raise InvalidWordError(ERR_INVALID_WORD.format(WORD_LENGTH, "9" * WORD_LENGTH, "9" * WORD_LENGTH))
                break
            except InvalidWordError as e:
                print(str(e))
            except EOFError:
                print("\nPlease enter input on the last line of the console. Try again.")

        self.memory[operand] = f"{int(word):+07d}"
    
    def write_op(self, operand: int):
        print(self.memory[operand])
    
    def load_op(self, operand: int):
        self.accumulator = int(self.memory[operand])
    
    def store_op(self, operand: int):
        self.memory[operand] = f"{self.accumulator:+07d}"
    
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
        opcode = self.get_opcode(self.program_counter)
        operand = int(code[4:7])

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
        
class ProgramLoader:
    @staticmethod
    def validate_code_format(code: str):
        if len(code) != 7 or code[0] not in ('+', '-') or not code[1:].isdigit():
            raise InvalidWordError(f"Invalid instruction: {code}")

    def load(self, vm: VM, filepath: str):
        user_program = ["+" + ("0" * WORD_LENGTH)] * MEMORY_LENGTH
        has_halt = False
        with open(filepath, "r") as f:
            lines = f.readlines()
            if len(lines) > MEMORY_LENGTH:
                raise MemoryError(ERR_PROGRAM_TOO_LARGE)
            
            for i, line in enumerate(lines):
                code = line.strip()
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
            self.validate_code_format(code)
            vm.memory[i] = code
    
    def force_load(self, filepath: str, object):
        object.memory = []
        with open(filepath, "r") as f:
            lines = f.readlines()
        
        for line in lines:
            code = line.strip()
            object.memory.append(code)

if __name__ == "__main__":
    vm = VM()
    pl = ProgramLoader()
    pl.load(vm, "test_files/6-digit-test.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)