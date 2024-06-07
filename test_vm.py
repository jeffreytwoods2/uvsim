import unittest
from unittest.mock import patch
from io import StringIO
from vm import VM

class TestRead(unittest.TestCase):
    @patch("vm.input", return_value="1")
    def test_positive_num(self, mock_input):
        vm = VM()
        vm.read_op(2)
        assert vm.memory[2] == "+0001"

    @patch("vm.input", return_value="-1")
    def test_negative_num(self, mock_input):
        vm = VM()
        vm.read_op(2)
        assert vm.memory[2] == "-0001"

class TestWrite(unittest.TestCase):
    @patch("sys.stdout", new_callable=StringIO)
    def test_positive_value(self, mock_stdout):
        vm = VM()
        vm.memory[0] = "+0001"
        vm.write_op(0)
        self.assertEqual(mock_stdout.getvalue().strip(), "+0001")
    
    @patch("sys.stdout", new_callable=StringIO)
    def test_negative_value(self, mock_stdout):
        vm = VM()
        vm.memory[0] = "-0001"
        vm.write_op(0)
        self.assertEqual(mock_stdout.getvalue().strip(), "-0001")

class TestLoad(unittest.TestCase):
    # Test loading values into the accumulator
    def test_load_positive(self):
        vm = VM()
        vm.memory = [
            "+0001",
            "-0023",
            "+0045"
        ]
        vm.load_op(0)  # Load +0001 into accumulator
        assert vm.accumulator == 1
    
    def test_load_negative(self):
        vm = VM()
        vm.memory = [
            "+0001",
            "-0023",
            "+0045"
        ]
        vm.load_op(1)  # Load -0023 into accumulator
        assert vm.accumulator == -23

class TestStore(unittest.TestCase):
    # Test storing values from the accumulator into memory
    def test_store_positive(self):
        vm = VM()
        vm.accumulator = 67
        vm.store_op(2)  # Store +0067 at index 2
        assert vm.memory[2] == ("+0067")

    def test_store_negative(self):
        vm = VM()
        vm.accumulator = -89
        vm.store_op(2) # Store -0089 at index 2
        assert vm.memory[2] == ("-0089")

class TestAddition(unittest.TestCase):
    def test_addition1(self):
        vm = VM()
        vm.memory[50] = "+0003"
        vm.add_op(50)
        assert vm.accumulator == 3 # 0 + 3

    def test_addition2(vm):
        vm = VM()
        vm.accumulator = 3
        vm.memory[50] = "+0040"
        vm.add_op(50)
        assert vm.accumulator == 43 # 3 + 40

class TestSubtraction(unittest.TestCase):
    def test_subtraction1(self):
        vm = VM()
        vm.memory[50] = "+0023"
        vm.subtract_op(50)
        assert vm.accumulator == -23 # 0 - 23

    def test_subtraction2(self):
        vm = VM()
        vm.accumulator = 23
        vm.memory[50] = "+0015"
        vm.subtract_op(50)
        assert vm.accumulator == 8 # 23 - 15

class TestDivision(unittest.TestCase):
    def test_division1(self):
        vm = VM()
        vm.accumulator = 30
        vm.memory[0] = "+0003"
        vm.divide_op(0)
        assert vm.accumulator == 10 # 30 / 3

    def test_division2(self):
        vm = VM()
        vm.accumulator = 10
        vm.memory[50] = "+0005"
        vm.divide_op(50)
        assert vm.accumulator == 2 # 10 / 5

class TestMultiplication(unittest.TestCase):
    def test_multiplication1(self):
        vm = VM()
        vm.accumulator = 5
        vm.memory[0] = "+0003"
        vm.multiply_op(0) # 0 is the memory address where the operand lies
        assert vm.accumulator == 15 # 5 * 3

    def test_multiplication2(self):
        vm = VM()
        vm.accumulator = 15
        vm.memory[50] = "+0002"
        vm.multiply_op(50)
        assert vm.accumulator == 30 # 15 * 2

class TestBranch(unittest.TestCase):
    # VM branches with valid address
    def test_1(self):
        vm = VM()
        vm.branch_op(10)
        assert(vm.program_counter == 10)
    
    # Invalid jump address rejected
    def test_2(self):
        vm = VM()
        with self.assertRaises(Exception):
            vm.branch_op(-1)

class TestBranchNeg(unittest.TestCase):
    # Correctly branches with negative accumulator
    def test_1(self):
        vm = VM()
        vm.accumulator = -1
        vm.branchneg_op(10)
        assert(vm.program_counter == 10)
    
    # Doesn't branch if accumulator is positive
    def test_2(self):
        vm = VM()
        vm.accumulator = 1
        vm.branchneg_op(10)
        assert(vm.program_counter != 10)

class TestBranchZero(unittest.TestCase):
    # Correctly branches when accumulator == 0
    def test_1(self):
        vm = VM()
        vm.accumulator = 0
        vm.branchzero_op(10)
        assert(vm.program_counter == 10)
    
    # Doesn't branch if accumulator = 0
    def test_2(self):
        vm = VM()
        vm.accumulator = 1
        vm.branchzero_op(10)
        assert(vm.program_counter != 10)

class TestHalt(unittest.TestCase):
    # Halt instruction terminates program immediately
    def test_1(self):
        vm = VM()
        vm.memory[0] = "+4300"
        vm.memory[1] = "+4050"
        vm.run()
        assert(vm.program_counter != 50)
    
    # Halt instruction works anywhere in memory
    def test_2(self):
        vm = VM()
        vm.memory[0] = "+4050"
        vm.memory[50] = "+4300"
        vm.run()
        assert(vm.program_counter == 51)

class TestLoadProgram(unittest.TestCase):
    # Code correctly loads into VM
    def test_1(self):
        vm = VM()
        vm.load_program("test_files/Test1.txt")
        with open("test_files/Test1.txt", "r") as f:
            lines = f.readlines()
            
            for i in range(len(lines)):
                file_code = lines[i].strip()
                vm_code = vm.memory[i]
                assert(file_code == vm_code)
    
    # File is rejected if larger than VM capacity
    def test_2(self):
        vm = VM()
        with self.assertRaises(Exception):
            vm.load_program("test_files/TooLong.txt")

class TestRun(unittest.TestCase):
    # Correctly executes first and last instruction in a max-length program
    def test_1(self):
        vm = VM()
        vm.load_program("test_files/FullProgram.txt")
        vm.run()
        assert(vm.program_counter == 100)

    # Throws error on invalid opcode
    def test_2(self):
        vm = VM()
        vm.memory[0] = "+9900"
        with self.assertRaises(Exception):
            vm.run()

if __name__ == "__main__":
    unittest.main()