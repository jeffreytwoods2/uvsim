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
install the following module with pip:
	pip install customtkinter
	Update existing installation: pip install customtkinter --upgrade
 (Reminder: format better later)

### Installing uvsim:
From uvsim's root page on GitHub, click on the green __<> Code__ button. This will open up a small menu, at the bottom of which you will need to click __Download ZIP__. This will download a __.zip__ folder with all of the necessary files onto your local machine. Go ahead and extract them into a directory of your choice.

### Running uvsim:
To run uvsim, start by opening a new terminal or command line window. If you are using Windows, make sure to open your terminal application as an administrator. Then, navigate to the __uvsim_master__ directory (the location of this directory will depend on where you extracted the __.zip__ file). A virtual environment configuration exists to ensure that the Python packages necessary for this program do not conflict with any that may be saved on your machine. Before attempting to run the program, perform the following steps to enter the virtual environment:

#### Windows
1. In Powershell and related terminals, type `.\bin\Activate.ps1`. In CMD Prompt, type `.\bin\activate.bat`.
2. Run the command `pip install -r requirements.txt`.
3. To exit the virtual environment when you are done using the program, type `deactivate`.

#### Mac/Linux
1. Run the command `source ./bin/activate`.
2. Run `pip install -r requirements.txt`.
3. When you are finished, run `deactivate`.

MacOS may not be able to run the custom Tkinter package inside of the venv depending on how you installed Python. If you use homebrew to install python-tk, the Tkinter package should then work correctly in venv.

Finally, run the command `python3 main.py` If this doesn't work, you can also try replacing __python3__ with just __python__, or whichever version of python you have installed.

Alternatively, you can use __VS Code__ to run it. To do so, make sure you have the Python extension installed before opening the __uvsim_master__ directory. Once you have the `main.py` file open, run it by using the play button in the top-right corner of the editor,

If you are using VS Code to run  the program and customtkinter is not recognized after you installed it, this might be caused by an incorrect Python interpreter
You can use shortcuts "Ctrl+Shift+P" and type "Python: Select Interpreter" to choose your virtual environment.

### Using uvsim:
Once the program is up and running, start by clicking on the __Import File__ button to select a file from your computer that you would like to run as the program. You can also click on the __Program Editor__ button which allows you to edit the contents of a file you've uploaded, or write a program completely from scratch. Once you've loaded your program into the system - either through a file import or manually - click on the __Run Program__ button to execute your program's instructions.

Any keyboard input requests from the program will appear in the __Console__. Click into the console, ensure that you cursor is below all text on its own newline, and then type the requested input. Press __Enter__ to submit your input to the program.

In the __Memory__ section of the GUI window, you will see the entire contents of the machine's 100-address memory; the memory will always stay up to date as the machine progresses through each program, keeping you informed of the machine's current state at any given time.

In the __Status__ section, you will see the value currently loaded in the accumulator. The accumulator serves as temporary storage for the results of operations; at the end of all relevant operations, the value is most often stored back in memory. Beneath the accumulator is the Program Counter; this register points to whichever instruction the machine will execute next. You can keep an eye on the Program Counter as it updates live to debug and verify the execution of your program.

If you've altered a program with the Program Editor and you'd like to save it as a new file, click __Save File__. A dialog window will open, allowing you to select the filename you'd like as well as the directory to save it in. The file extension should be set automatically, but if it isn't on your system, make sure to set it to ".txt", as this is the only file type that the VM accepts.

When you have finished running a program, you can load another using the steps mentioned above, and all fields in the GUI will clear their outdated contents and load in values from the new program.

When you are done using UVSim, click the __Close__ button at the top to terminate the program (exact details of the button will vary by platform).

### Note on input files:
If you want to process your own program through uvsim, check the files in __test_files__ to get an idea of what the program should look like. Note that the format for each line of your program should be either `+` or `-`, followed by the 4-digit instruction (see above for details on each instruction).
