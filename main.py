<<<<<<< HEAD
accumulator = 0

# To test functions where accumulator is altered
def get_accumulator():
    return accumulator

#Read a word from the keyboard into a specific location in memory
def read_op(memory_list, operand):
    word = input()
    try:
        if int(word) > 9999 or int(word) < -9999:
            print('Please enter a four digit word')
    except:
        print('Please enter a four digit word')

    if int(word) < 0:
        memory_list[operand] = ('-',str(word).zfill(4))
    else:
        memory_list[operand] = ('+',str(word).zfill(4))

#Write a word from a specific location in memory to screen
def write_op(memory_list, operand):
    print(memory_list[operand][0] + memory_list[operand][1])

#Load a word from a specific location in memory into the accumulator
def load_op():
    pass

#Store a word from the accumulator into a specific location in memory
def store_op():
    pass

#Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
def add_op(operand):
    global accumulator
    accumulator += operand

#Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
def subtract_op(operand):
    global accumulator
    accumulator -= operand

#Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator)
def divide_op(operand):
    global accumulator
    accumulator /= operand

#multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
def multiply_op(operand):
    global accumulator
    accumulator *= operand


def iterate_list(memory_list, start_index):
    for i in range(start_index, len(memory_list)):
        op = memory_list[i][1][0:2]
        operand = int(memory_list[i][1][2:4])
        match op:
            case '10':
                read_op(memory_list, operand)
            case '11':
                write_op(memory_list, operand)
            case '20':
                load_op()
            case '21':
                store_op()
            case '30': 
                add_op(int(memory_list[operand][1]))
            case '31':
                subtract_op(int(memory_list[operand][1]))
            case '32':
                divide_op(int(memory_list[operand][1]))
            case '33':
                multiply_op(int(memory_list[operand][1]))
            #Branch to a specific location in memory
            case '40':
                iterate_list(memory_list, operand)
                break
            #Branch to a specific location in memory if the accumulator is negative
            case '41':
                pass
            #Branch to a specific location in memory if the accumulator is negative
            case '42':
                pass
            #Stop the program
            case '43':
                pass
            case _:
                pass
=======
from vm import VM
>>>>>>> 5ab9c68cee53802e85e8c074daf3614e72a5cf5a

def main():
    vm = VM()
    vm.load_program("test_files/Test2.txt")
    vm.run()
    print("\nFINAL STATE")
    print(vm)

<<<<<<< HEAD
    while True:
        if len(memory_contents) > 99:
            break
        
        line = file.readline().strip()
     
        if not line:
            break

        #check for file format
        valid_unsigned = True
        try:
            int(line[1:4])
        except:
            valid_unsigned = False

        if len(line) != 5 or (line[0] != '+' and line[0] != '-') or valid_unsigned == False:
            print("Invlaid file format")
            return
        
        #append entry to memory contents
        memory_contents.append((line[0],line[1:5] ))

    file.close()
    print(memory_contents)
    iterate_list(memory_contents, 0)

if __name__ == "__main__":
    main()
=======
main()
>>>>>>> 5ab9c68cee53802e85e8c074daf3614e72a5cf5a
