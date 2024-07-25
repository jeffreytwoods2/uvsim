import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk, WORD
import sys
import threading
from queue import Queue
from vm import VM, ProgramLoader
from program_edit_window import ProgramEditor
from text_redirector import TextRedirector, InputRedirector
from config import *

class VMHeader(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=("Helvetica", 20, "bold"))

class VMApp(ctk.CTkFrame):
    def __init__(self, master, tabview):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.tabview = tabview
        self.is_running = False

        self.vm = VM()
        self.pl = ProgramLoader()
        self.program_editor = ProgramEditor(self)
        self.waiting_for_input = False

        # Create a StringVar to hold the console output
        self.console_output = ctk.StringVar()
        self.console_output.trace_add('write', self.update_console)

        # Configure the main grid layout
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Create and populate the left frame (Memory and control buttons)
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=18, pady=20, sticky="nsew")
        self.populate_left_frame()

        # Create and populate the right frame (Status and Console)
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=18, pady=20, sticky="nsew")
        self.populate_right_frame()

        self.setup_input_redirection()
        # Set VM input and output functions
        self.vm.set_io_functions(self.input_redirector.readline, self.output_redirector.write)
        # Update the GUI to reflect the initial state of the VM
        self.update_screen()
        self.update_memory_tree()
    
    def populate_left_frame(self):
        # Configure the grid layout for the left frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        # Add the "Memory" header
        VMHeader(self.left_frame, text="Memory").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Helvetica', 20), rowheight=30)
        style.configure("Custom.Treeview.Heading", font=('Helvetica', 22, 'bold'))

        # Create a frame to hold the Treeview and Scrollbar
        tree_frame = ctk.CTkFrame(self.left_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Create the Treeview
        self.memory_tree = ttk.Treeview(tree_frame, columns=("Address", "Value"),
            show="headings", style="Custom.Treeview")
        
        self.memory_tree.heading("Address", text="Address")
        self.memory_tree.heading("Value", text="Value")
        self.memory_tree.column("Address", anchor="center", width=180)
        self.memory_tree.column("Value", anchor="center", width=180)
        self.memory_tree.grid(row=0, column=0, sticky="nsew")

        # Create the Scrollbar
        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.memory_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the Treeview to use the Scrollbar
        self.memory_tree.configure(yscrollcommand=scrollbar.set)

        # Create a frame for the control buttons
        button_frame = ctk.CTkFrame(self.left_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=(10,25), pady=10)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Add control buttons: Import File, Run Program, and Program Editor
        ctk.CTkButton(button_frame, text="Import File", command=self.select_file).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Run Program", command=self.run_from_start).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Program Editor", command=self.open_program_editor).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Save File", command=self.save_file).grid(row=1, column=0, padx=5, pady=5)

    def populate_right_frame(self):
        # Configure the grid layout for the right frame
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)

        # Create and populate the status section
        status_frame = ctk.CTkFrame(self.right_frame)
        status_frame.grid(row=0, column=0, padx=(15,5), pady=10, sticky="ew")
        VMHeader(status_frame, text="Status").pack(anchor="w")
        self.accumulator_label = ctk.CTkLabel(status_frame, text=f"Accumulator: {self.vm.accumulator}")
        self.accumulator_label.pack(anchor="w")
        self.pc_label = ctk.CTkLabel(status_frame, text=f"Program Counter: {self.vm.program_counter}")
        self.pc_label.pack(anchor="w")

        # Add the "Console" header
        VMHeader(self.right_frame, text="Console").grid(row=1, column=0, sticky="w", padx=10, pady=(5, 0))
        
        # Create and configure the console text box
        self.console_text = ctk.CTkTextbox(self.right_frame, height=200, width=300, wrap=WORD)
        self.console_text.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.console_text.bind("<Return>", self.on_enter_pressed)

        # Add the "Enter" button below the console
        self.enter_button = ctk.CTkButton(self.right_frame, text="Enter", command=self.on_enter_pressed)
        self.enter_button.grid(row=3, column=0, pady=(0, 10))

        # Display initial prompt
        self.display_prompt()

    def on_enter_pressed(self, event=None):
        if self.waiting_for_input:
            # Get the last line of text from the console (user input)
            input_start = self.console_text.index("end-1c linestart")
            command = self.console_text.get(f"{input_start}+2c", "end-1c")

            # Add a newline
            self.console_text.insert("end", "\n")
            # Pass the input to the input queue
            self.input_queue.put(command)
            # Reset waiting_for_input flag
            self.waiting_for_input = False
        else:
            # If not waiting for input, just add a newline
            self.console_text.insert("end", "\n")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if file_path == () or file_path == "":             
            return  # User cancelled file selection
        try:
            self.pl.load(self.vm, file_path)
            self.clear_all_fields()
            messagebox.showinfo("Success!", "Your program is loaded and ready to run")
        except Exception as details:
            messagebox.showerror("Invalid File", str(details))
        
        self.pl.force_load(file_path, self.program_editor)

    def save_file(self):
        contents = ""
        for item in self.program_editor.memory:
            contents += f"{item}\n"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=FILE_TYPES)
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(contents)
            except Exception as e:
                messagebox.showerror("Save Error", ERR_FILE_SAVE.format(str(e)))

    def display_prompt(self):
        if self.waiting_for_input:
            self.console_text.insert("end", ">")
        self.console_text.see("end")

    def update_memory_tree(self):
        # Populate the memory display with current VM memory contents
        if len(self.memory_tree.get_children()) == 0:
            for i, value in enumerate(self.vm.memory):
                address = f"{i:03d}"
                self.memory_tree.insert("", "end", values=(address, value))
                self.style_memory_tree()
        
        # Update any differences between memory tree and vm memory
        else:
            for i, item in enumerate(self.memory_tree.get_children()):
                self.memory_tree.item(item, values=(f"{i:03d}", self.vm.memory[i]))
                
    def update_screen(self):
        # Update the accumulator and program counter labels
        self.accumulator_label.configure(text=f"Accumulator: {self.vm.accumulator}")
        self.pc_label.configure(text=f"Program Counter: {self.vm.program_counter}")
        
        # Ensure the console is scrolled to the bottom
        self.console_text.see("end")

    def style_memory_tree(self):
        # Apply alternating row colors to the memory display
        self.memory_tree.tag_configure('evenrow', background='lightgrey')
        for index, row in enumerate(self.memory_tree.get_children()):
            if index % 2 == 0:
                self.memory_tree.item(row, tags=('evenrow',))

    def clear_all_fields(self):
        # Reset the VM state
        self.vm.program_counter = 0
        self.vm.accumulator = 0
        # Clear the console
        self.console_text.delete("1.0", "end")
        # Update the GUI to reflect the changes
        self.update_screen()
        self.update_memory_tree()

    def check_for_memory_update(self):
        # Check to see if memory has been changed. If so, updates the memory tree
        last_opcode = self.vm.get_opcode(self.vm.program_counter - 1)

        # If previous action was load or store, then the tree needs to be udpated
        if last_opcode == "010" or last_opcode == "021":
            self.update_memory_tree()

    def run_from_start(self):
        def run_program():
            self.is_running = True
            # Redirect stdout to this tab's console
            original_stdout = sys.stdout
            original_stdin = sys.stdin
            sys.stdout = self.output_redirector
            sys.stdin = self.input_redirector
            
            self.clear_all_fields()
            try:
                self.vm.run()
            except Exception as e:
                self.console_text.insert(ctk.END, f"Error: {str(e)}\n")
            finally:
                self.is_running = False
                sys.stdout = original_stdout
                sys.stdin = original_stdin
                self.update_screen()
                self.update_memory_tree()

        threading.Thread(target=run_program, daemon=True).start()

    def open_program_editor(self):
        # Open the program editor window
        self.program_editor.open()
        
    def setup_input_redirection(self):
        self.input_queue = Queue()
        self.input_redirector = InputRedirector(self.input_queue, self)
        self.output_redirector = TextRedirector(self.console_output, self, "stdout")

    def update_console(self, *args):
        self.console_text.insert(ctk.END, self.console_output.get())
        self.console_text.see(ctk.END)
        self.console_output.set('')