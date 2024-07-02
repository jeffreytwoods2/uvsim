# uvsim
An educational virtual machine running BasicML

## Overview
UVSim is a virtual machine implemented in Python for computer science students to learn machine language and computer architecture.

The VM runs a low-level language called BasicML to help students learn the basic concepts behind assembly and machine languages.

## Hardware
UVSim contains a CPU, main memory, and registers, including an accumulator to store the results of operations before saving to memory.

## BasicML
The entirety of BasicML is specified as follows:

### I/O operations:

READ = 10 Read a word from the keyboard into a specific location in memory.

WRITE = 11 Write a word from a specific location in memory to screen.

### Load/store operations:

LOAD = 20 Load a word from a specific location in memory into the accumulator.

STORE = 21 Store a word from the accumulator into a specific location in memory.

### Arithmetic operations:

ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)

SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)

DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).

MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

### Control operations:

BRANCH = 40 Branch to a specific location in memory

BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.

BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.

HALT = 43 Stop the program

The last two digits of a BasicML instruction are the operand – the address of the memory location containing the word to which the operation applies

## Getting Started on uvsim:
Note: To run this software, you will need Python installed on your local machine.

### Installing uvsim:
From uvsim's root page on GitHub, click on the green __<> Code__ button. This will open up a small menu, at the bottom of which you will need to click __Download ZIP__. This will download a __.zip__ folder with all of the necessary files onto your local machine. Go ahead and extract them into a directory of your choice.

### Running uvsim:
To run uvsim, start by opening a new terminal or command line window. Then, navigate to the __uvsim_master__ directory (the location of this directory will depend on where you extracted the __.zip__ file). Finally, run the command `python3 main.py` If this doesn't work, you can also try replacing __python3__ with just __python__, or whichever version of python you have installed.

Alternatively, you can use __VS Code__ to run it. To do so, make sure you have the Python extension installed before opening the __uvsim_master__ directory. Once you have the `main.py` file open, run it by using the play button in the top-right corner of the editor,

### Using uvsim:
Once the program is up and running, start by clicking on the __Import File__ button to select a file from your computer that you would like to run as the program. You can also click on the __Program Editor__ button which allows you to edit the contents of a file you've uploaded, or write a program completely from scratch. Once you've loaded your program into the system - either through a file import or manually - click on the __Run Program__ button to execute your program's instructions.

### Note on input files:
If you are wanting to process your own program through uvsim, check the files in __test_files__ to get an idea of what the program should look like. Note that the format for each line of your program should be either `+` or `-`, followed by the 4-digit instruction (see above for details on each instruction).
