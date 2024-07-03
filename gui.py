import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from vm import VM, ProgramLoader
from program_edit_window import ProgramEditor
import sys
import threading

# Custom Label class for VM headers
class VMHeader(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=("Helvetica", 16, "bold"), pady=10)

# Main application class for the VM GUI
class VMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VM")
        self.vm = VM() # Initialize the Virtual Machine
        self.pl = ProgramLoader() # Initialize the Program Loader
        self.program_editor = ProgramEditor(self) # Initialize the Program Editor

        # Create main container
        self.container = tk.Frame(self.root)
        self.container.pack(pady=50, padx=20)

        # Create memory container
        self.memory_container = tk.Frame(self.container)
        self.memory_container.pack(side=tk.LEFT, padx=20, pady=30)

        # Create status and console container
        status_console_container = tk.Frame(self.container)
        status_console_container.pack(padx=20, pady=30)

        # Create status container
        self.status_container = tk.Frame(status_console_container)
        self.status_container.pack(anchor=tk.NW)

        # Create console container
        self.console_container = tk.Frame(status_console_container)
        self.console_container.pack(pady=30)

        # Populate the GUI components
        self.populate_memory_container()
        self.populate_accumulator_container()
        self.populate_console_container()
        self.update_screen()

        # Redirect stdout to the GUI console
        sys.stdout = TextRedirector(self.textbox, "stdout")
        # Set up input redirection
        self.input_redirector = InputRedirector(self)
        sys.stdin = self.input_redirector

    # Create and populate the memory display
    def populate_memory_container(self):
        memory_title = tk.Label(self.memory_container, text="Memory")
        memory_title.pack(side=tk.TOP, anchor=tk.W)

        # Create frame for memory display
        memory_frame = tk.Frame(self.memory_container)
        memory_frame.pack()

        # Create a treeview to display memory contents
        self.memory_tree = ttk.Treeview(
            memory_frame,
            columns=("Address", "Value"),
            show="headings",
            height=20 # Display 20 rows at a time
        )
        self.memory_tree.heading("Address", text="Address")
        self.memory_tree.heading("Value", text="Value")

        # Set column widths and center alignment
        self.memory_tree.column("Address", anchor=tk.CENTER, width=180)
        self.memory_tree.column("Value", anchor=tk.CENTER, width=180)
        
        self.memory_tree.pack()

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.memory_container)
        button_frame.pack(pady=10)

        # Add buttons for importing files, running programs, and opening the program editor
        select_file_button = tk.Button(button_frame, text="Import File", command=self.select_file)
        select_file_button.pack(side=tk.LEFT, padx=5)

        run_button = tk.Button(button_frame, text="Run Program", command=self.run_from_start)
        run_button.pack(side=tk.LEFT, padx=5)

        update_button = tk.Button(button_frame, text="Program Editor", command=self.open_program_editor)
        update_button.pack(side=tk.LEFT, padx=5)

    # Apply alternating row colors to the memory display
    def style_memory_tree(self):
        self.memory_tree.tag_configure('evenrow', background='lightgrey')
        for index, row in enumerate(self.memory_tree.get_children()):
            if index % 2 == 0:
                self.memory_tree.item(row, tags=('evenrow',))

    # Create and populate the accumulator and program counter display
    def populate_accumulator_container(self):
        VMHeader(self.status_container, text="Status").pack(anchor=tk.NW)

        # Add accumulator display
        self.accumulator_label = tk.Label(self.status_container, text=f"Accumulator: {self.vm.accumulator}")
        self.accumulator_label.pack(anchor=tk.NW)

        # Add program counter display
        self.pc_label = tk.Label(self.status_container, text=f"Program Counter: {self.vm.program_counter}")
        self.pc_label.pack()

    # Create and populate the console display
    def populate_console_container(self):
        console_header = VMHeader(self.console_container, text="Console")
        console_header.pack(anchor=tk.W)

        # Create text widget for console display and input
        self.textbox = tk.Text(self.console_container, height=18, width=40)
        self.textbox.pack()

        # Bind Enter key to input handling
        self.textbox.bind("<Return>", self.on_enter_pressed)

        # Add "Enter" button for input
        enter_button = tk.Button(self.console_container, text="Enter", command=self.on_enter_pressed)
        enter_button.pack(pady=5)

    # Handle Enter key press in the console
    def on_enter_pressed(self, event=None):
        # Get the last line of text (user input)
        command = self.textbox.get("end-1c linestart", "end-1c lineend")
        # Pass input to the input redirector
        self.input_redirector.set_input(command)
        # Add newline for visual feedback
        self.textbox.insert("end", "\n")

    # Open a file dialog to select and load a program
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path == () or file_path == "":             
            return # User cancelled file selection
        try:
            # Attempt to load the selected file
            self.pl.load(self.vm, file_path)
            messagebox.showinfo("Success!", "Your program is loaded and ready to run")
        except Exception as details:
            messagebox.showerror("Invalid File", details) 
        
        self.pl.force_load(file_path, self.program_editor)

    # Update the GUI to reflect the current state of the VM
    def update_screen(self):
        # Clear and repopulate the memory display
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)

        # Populate memory display with current VM memory contents
        for i, value in enumerate(self.vm.memory):
            address = f"{i:02d}"
            self.memory_tree.insert("", "end", values=(address, value))
        self.style_memory_tree()

        # Update accumulator and program counter labels
        self.accumulator_label.config(text=f"Accumulator: {self.vm.accumulator}")
        self.pc_label.config(text=f"Program Counter: {self.vm.program_counter}")

    #Clear all fields and reset the VM state.
    def clear_all_fields(self):
        # Reset VM state
        self.vm.program_counter = 0
        self.vm.accumulator = 0
        # Clear console
        self.textbox.delete("1.0", "end")
        self.update_screen()

    # Run the loaded program from the start
    def run_from_start(self):
        def run_program():
            self.clear_all_fields()
            # Run program step by step, updating GUI after each step
            for _ in self.vm.run_by_step():
                self.update_screen()
            self.update_screen()

        threading.Thread(target=run_program).start()

    # Open the program editor window
    def open_program_editor(self):
        self.program_editor.open()

# Class to redirect stdout to the GUI console
class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    # Write output to text widget
    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string, (self.tag,))
        self.widget.update()

    # Required for file-like objects, no action needed
    def flush(self):
        pass

# Class to handle input redirection from the GUI console
class InputRedirector:
    def __init__(self, app):
        self.app = app
        self.input_ready = threading.Event()
        self.input_value = None

    # Set input value and signal that input is ready
    def set_input(self, value):
        self.input_value = value
        self.input_ready.set()

    # Wait for input to be ready, then return it
    def readline(self):
        self.input_ready.wait()
        self.input_ready.clear()
        return self.input_value

# Main entry point of the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VMApp(root)
    root.mainloop()
