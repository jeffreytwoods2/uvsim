# Software Requirement Specification 

## Functional Requirements 

1. The system shall implement a READ operation where a word input from the keyboard is stored in a specific location in memory. 

 

2. The system shall implement a WRITE operation where a word from a specific location in memory is shown on the screen. 

3. The system shall implement a LOAD operation where a word from a specific location in memory is loaded into the system’s accumulator. 

4. The system shall implement a STORE operation where the word in the accumulator is stored in a specific location in memory.  

5. The system shall implement an ADD operation where a word from a specific location in memory is added to the accumulator 

6. The system shall implement a SUBTRACT operation where a word from a specific location in memory is subtracted from the accumulator.  

7. The system shall implement a DIVIDE operation where the accumulator is divided by a word from a specific location in memory.  

8. The system shall implement a MULTIPLY operation where the accumulator is multiplied by a word from a specific location in memory.  

9. The system shall have a graphical user interface displaying the program counter, accumulator, memory, and output values.  

10. The system shall provide a memory capacity of 100 words, each word being a 4- digit signed integer. 

11. The system shall have an accumulator register to store and manipulate values during execution. 

12. The system shall have a program counter to keep track of the current instruction being executed. 

13. The system shall accept and execute the full range of the UVSIM instruction set architecture. 

14. The system shall allow the user to select a file from his/her local machine to be processed by the simulator.  

15. The system shall load the input file’s contents into its memory after a properly formatted file is provided. 

16. The system shall handle negative values using a 4-digit representation with a leading minus sign, and positive values with a leading plus sign. 

17. The system shall truncate overflowing integer values before saving them to memory. 

18. The system shall truncate underflowing integer values before saving them to memory. 

19. The system shall validate branch addressed to ensure they are within the valid memory range. 

20. The system shall refuse to load a program that lacks at least one HALT instruction to avoid infinite loops. 

21. The system shall output a warning message upon receiving invalid user input 

22. The system shall repeat a request for user input until a valid input is provided. 

23. The system shall display the final state of the virtual machine upon program termination.  

## Non-Functional Requirements 

1. The system shall be platform-independent and capable of running on Mac, Linux, and Windows operating systems without modification. 

2. The system shall initialize and be available for user input in under three seconds. 

3. The system shall be implemented in Python and follow the best coding practices, including modular design and error handling.  