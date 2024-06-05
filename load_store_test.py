from main import load_op, store_op, get_accumulator

# Simulated memory for testing
test_memory = [
    ('+', '0001'),
    ('-', '0023'),
    ('+', '0045')
]

# Test loading values into the accumulator
def test_load_positive():
    load_op(test_memory, 0)  # Load +0001 into accumulator
    assert get_accumulator() == 1

def test_load_negative():
    load_op(test_memory, 1)  # Load -0023 into accumulator
    assert get_accumulator() == -23

# Test storing values from the accumulator into memory
def test_store_positive():
    global accumulator
    accumulator = 67
    store_op(test_memory, 2)  # Store +0067 at index 2
    assert test_memory[2] == ('+', '0067')

def test_store_negative():
    global accumulator
    accumulator = -89
    store_op(test_memory, 2)  # Store -0089 at index 2
    assert test_memory[2] == ('-', '0089')
