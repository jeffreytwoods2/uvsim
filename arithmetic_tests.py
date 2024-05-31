from main import add_op, subtract_op, multiply_op, divide_op, get_accumulator

# Test addition
def test_addition1():
    add_op(3)
    assert get_accumulator() == 3 # 0 + 3

def test_addition2():
    add_op(40)
    assert get_accumulator() == 43 # 3 + 40

# Test subtraction
def test_subtraction1():
    subtract_op(23)
    assert get_accumulator() == 20 # 43 - 23

def test_subtraction2():
    subtract_op(15)
    assert get_accumulator() == 5 # 20 - 15

# Test multiplication
def test_multiplication1():
    multiply_op(3)
    assert get_accumulator() == 15 # 5 * 3

def test_multiplication2():
    multiply_op(2)
    assert get_accumulator() == 30 # 15 * 2

# Test division
def test_division1():
    divide_op(3)
    assert get_accumulator() == 10 # 30 / 10

def test_division2():
    divide_op(5)
    assert get_accumulator() == 2 # 10 / 5
