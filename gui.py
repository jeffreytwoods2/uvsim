import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk, WORD
import sys
import threading
from queue import Queue
from vm import VM, ProgramLoader
from program_edit_window import ProgramEditor
from json.decoder import JSONDecodeError

# Custom header label for sections in the GUI
class VMHeader(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=("Helvetica", 20, "bold"))

# Main application class for the VM Simulator
class VMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VM Simulator")
        
        # Set initial window size
        window_width = 800
        window_height = 600
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        # Center the window on the screen
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Set the appearance mode custom color theme
        # The try block is for unit test purposes
        try:
            ctk.set_default_color_theme("theme.json")
            ctk.set_appearance_mode("dark")
        except JSONDecodeError:
            pass

        #Set backgroud color of the window
            self.root.configure(fg_color="gray87")

        # Initialize the Virtual Machine and Program Loader
        self.vm = VM()
        self.pl = ProgramLoader()
        self.program_editor = ProgramEditor(self)
        self.waiting_for_input = False

        # Configure the main grid layout
        # The left column (index 0) has a weight of 3, making it wider than the right column
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        # Create and populate the left frame (Memory and control buttons)
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(row=0, column=0, padx=18, pady=20, sticky="nsew")
        self.populate_left_frame()

        # Create and populate the right frame (Status and Console)
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.grid(row=0, column=1, padx=18, pady=20, sticky="nsew")
        self.populate_right_frame()

        # Set up input redirection for the console
        self.input_queue = Queue()
        self.input_redirector = InputRedirector(self.input_queue, self)
        sys.stdin = self.input_redirector

        # Redirect standard output to the GUI console
        sys.stdout = TextRedirector(self.console_text, self, "stdout")

        # Update the GUI to reflect the initial state of the VM
        self.update_screen()

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
        # Open a file dialog for the user to select a program file
        file_path = filedialog.askopenfilename()
        if file_path == () or file_path == "":             
            return  # User cancelled file selection
        try:
            # Attempt to load the selected file into the VM
            self.pl.load(self.vm, file_path)
            self.clear_all_fields()
            messagebox.showinfo("Success!", "Your program is loaded and ready to run")
        except Exception as details:
            messagebox.showerror("Invalid File", details) 
        
        # Force load the file into the program editor
        self.pl.force_load(file_path, self.program_editor)

    def display_prompt(self):
        if self.waiting_for_input:
            self.console_text.insert("end", "> ")
        self.console_text.see("end")

    def update_screen(self):
        # Clear the existing memory display
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)

        # Populate the memory display with current VM memory contents
        for i, value in enumerate(self.vm.memory):
            address = f"{i:03d}"
            self.memory_tree.insert("", "end", values=(address, value))
        self.style_memory_tree()

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

    def run_from_start(self):
        def run_program():
            # Clear all fields before running the program
            self.clear_all_fields()
            # Run the program step by step, updating the GUI after each step
            for _ in self.vm.run_by_step():
                self.update_screen()
            # Final update after program completion
            self.update_screen()

        # Run the program in a separate thread to keep the GUI responsive
        threading.Thread(target=run_program).start()

    def open_program_editor(self):
        # Open the program editor window
        self.program_editor.open()
    
    def save_file(self):
        # Save the contents of the user program as a txt
        contents = ""
        for item in self.program_editor.memory:
            contents += f"{item}\n"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(contents)

# Class to redirect stdout to the GUI console
class TextRedirector:
    def __init__(self, widget, app, tag="stdout"):
        self.widget = widget
        self.app = app
        self.tag = tag

    def write(self, string):
        self.widget.insert("end", string, (self.tag,))
        self.widget.see("end")
        # Only display a prompt if we're waiting for input
        if self.app.waiting_for_input:
            self.app.display_prompt()

    def flush(self):
        # Required for file-like objects, but no action needed
        pass

# Class to handle input redirection from the GUI console
class InputRedirector:
    def __init__(self, input_queue, app):
        self.input_queue = input_queue
        self.app = app

    def readline(self):
        self.app.waiting_for_input = True
        self.app.display_prompt()
        result = self.input_queue.get() + '\n'
        self.app.waiting_for_input = False
        return result

# Main entry point of the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = VMApp(root)
    root.mainloop()
