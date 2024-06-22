# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk, simpledialog
# from vm import VM, ProgramLoader
# import sys

# class VMHeader(tk.Label):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs, font=("Helvetica", 16, "bold"), pady=10)

# class VMApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("VM")
#         self.vm = VM()
#         self.pl = ProgramLoader()

#         self.container = tk.Frame(self.root)
#         self.container.pack(pady=50, padx=20)
        
#         self.memory_container = tk.Frame(self.container)
#         self.memory_container.pack(side=tk.LEFT, padx=20, pady=30)

#         status_console_container=tk.Frame(self.container)
#         status_console_container.pack(padx=20, pady=30)

#         self.status_container = tk.Frame(status_console_container)
#         self.status_container.pack(anchor=tk.NW)

#         self.console_container = tk.Frame(status_console_container)
#         self.console_container.pack(pady=30)

#         self.populate_memory_container()
#         self.populate_accumulator_container()
#         self.populate_console_container()
#         self.update_screen()

#         # Redirect stdout to the text box
#         sys.stdout = TextRedirector(self.textbox, "stdout")

#     def populate_memory_container(self):
#         # Add a title header to the memory frame
#         memory_title = VMHeader(self.memory_container, text="Memory")
#         memory_title.pack(side=tk.TOP, anchor=tk.W)

#         memory_frame = tk.Frame(self.memory_container)
#         memory_frame.pack()

#         # Add the memory slots to the frame
#         self.memory_tree = ttk.Treeview(
#             memory_frame,                   # memory_tree's "parent" element
#             columns=("Address", "Value"),
#             show="headings",
#             height=20                        # How many values will be shown at a time
#         )
#         self.memory_tree.heading("Address", text="Address")
#         self.memory_tree.heading("Value", text="Value")

#         # Center the column values
#         self.memory_tree.column("Address", anchor=tk.CENTER, width=180)
#         self.memory_tree.column("Value", anchor=tk.CENTER, width=180)
        
#         self.memory_tree.pack()

#         # Add a button to select a file
#         select_file_button = tk.Button(self.memory_container, text="Import File", command=self.select_file)
#         select_file_button.pack(pady=5)

#         # Add a button to run the program
#         run_button = tk.Button(self.memory_container, text="Run Program", command=self.run_from_start)
#         run_button.pack()

#     def style_memory_tree(self):
#         # Style tree rows
#         self.memory_tree.tag_configure('evenrow', background='lightgrey')
        
#         # Apply tags to rows
#         for index, row in enumerate(self.memory_tree.get_children()):
#             if index % 2 == 0:
#                 self.memory_tree.item(row, tags=('evenrow',))

#     def populate_accumulator_container(self):
#         VMHeader(self.status_container, text="Status").pack(anchor=tk.NW)
        
#         self.accumulator_label = tk.Label(self.status_container, text=f"Accumulator: {self.vm.accumulator}")
#         self.accumulator_label.pack(anchor=tk.NW)

#         self.pc_label = tk.Label(self.status_container, text=f"Program Counter: {self.vm.program_counter}")
#         self.pc_label.pack()
    
#     def populate_console_container(self):
#         console_header = VMHeader(self.console_container, text="Console")
#         console_header.pack(anchor=tk.W)

#         self.textbox = tk.Text(self.console_container, height=18, width=40)
#         self.textbox.pack()

#         # Bind the <Return> key to a callback function
#         self.textbox.bind("<Return>", self.on_enter_pressed)

#         enter_button = tk.Button(self.console_container, text="Enter", command=self.on_enter_pressed)
#         enter_button.pack(pady=5)

#     def on_enter_pressed(self, event=None):
#         # Event handler for when Enter key is pressed
#         command = self.textbox.get("1.0", "end-1c")  # Get the content of the text box
#         # Process the command as needed
#         self.textbox.delete("1.0", "end")  # Clear the text box after processing
#         # Perform further actions based on the entered command

#         # Example action: Display the command in the console
#         self.textbox.insert(tk.END, f"\nEntered command: {command}")

#         # Ensure the console view scrolls to the bottom to show latest input/output
#         self.textbox.see(tk.END)

#     def select_file(self):
#         file_path = filedialog.askopenfilename()
#         if file_path == () or file_path == "":             
#             return  # User cancelled import. Do not try to validate anything
        
#         try:
#             self.pl.load(self.vm, file_path)
#             self.update_screen()
#             messagebox.showinfo("Success!", "Your program is loaded and ready to run")
#         except Exception as details:
#             messagebox.showerror("Invalid File", details) 
    
#     def update_screen(self):
#         # Update Memory 
#         for item in self.memory_tree.get_children():
#             self.memory_tree.delete(item)

#         for i, value in enumerate(self.vm.memory):
#             if i < 10:
#                 address = "0" + str(i)
#             else:
#                 address = str(i)
#             self.memory_tree.insert("", "end", values=(address, value))
#         self.style_memory_tree()
        
#         # Update accumulator label and program counter label
#         self.accumulator_label.config(text=f"Accumulator: {self.vm.accumulator}")
#         self.pc_label.config(text=f"Program Counter: {self.vm.program_counter}")

#     def run_from_start(self):
#         self.vm.program_counter = 0

#         for _ in self.vm.run_by_step():
#             self.update_screen()
#         self.update_screen()

# class TextRedirector(object):
#     def __init__(self, widget, tag="stdout"):
#         self.widget = widget
#         self.tag = tag

#     def write(self, string):
#         self.widget.configure(state="normal")
#         self.widget.insert("end", string, (self.tag,))
#         self.widget.configure(state="disabled")
#         self.widget.update()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VMApp(root)
#     root.mainloop()



# import tkinter as tk
# from tkinter import filedialog, messagebox, ttk, simpledialog
# from vm import VM, ProgramLoader
# import sys
# import threading

# class VMHeader(tk.Label):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs, font=("Helvetica", 16, "bold"), pady=10)

# class VMApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("VM")
#         self.vm = VM()
#         self.pl = ProgramLoader()

#         self.container = tk.Frame(self.root)
#         self.container.pack(pady=50, padx=20)
        
#         self.memory_container = tk.Frame(self.container)
#         self.memory_container.pack(side=tk.LEFT, padx=20, pady=30)

#         status_console_container=tk.Frame(self.container)
#         status_console_container.pack(padx=20, pady=30)

#         self.status_container = tk.Frame(status_console_container)
#         self.status_container.pack(anchor=tk.NW)

#         self.console_container = tk.Frame(status_console_container)
#         self.console_container.pack(pady=30)

#         self.populate_memory_container()
#         self.populate_accumulator_container()
#         self.populate_console_container()
#         self.update_screen()

#         # Redirect stdout and stdin to the text box
#         sys.stdout = TextRedirector(self.textbox, "stdout")
#         self.input_redirector = InputRedirector(self)
#         sys.stdin = self.input_redirector

#     def populate_memory_container(self):
#         memory_title = VMHeader(self.memory_container, text="Memory")
#         memory_title.pack(side=tk.TOP, anchor=tk.W)

#         memory_frame = tk.Frame(self.memory_container)
#         memory_frame.pack()

#         self.memory_tree = ttk.Treeview(
#             memory_frame,
#             columns=("Address", "Value"),
#             show="headings",
#             height=20
#         )
#         self.memory_tree.heading("Address", text="Address")
#         self.memory_tree.heading("Value", text="Value")

#         self.memory_tree.column("Address", anchor=tk.CENTER, width=180)
#         self.memory_tree.column("Value", anchor=tk.CENTER, width=180)
        
#         self.memory_tree.pack()

#         select_file_button = tk.Button(self.memory_container, text="Import File", command=self.select_file)
#         select_file_button.pack(pady=5)

#         run_button = tk.Button(self.memory_container, text="Run Program", command=self.run_from_start)
#         run_button.pack()

#     def style_memory_tree(self):
#         self.memory_tree.tag_configure('evenrow', background='lightgrey')
#         for index, row in enumerate(self.memory_tree.get_children()):
#             if index % 2 == 0:
#                 self.memory_tree.item(row, tags=('evenrow',))

#     def populate_accumulator_container(self):
#         VMHeader(self.status_container, text="Status").pack(anchor=tk.NW)
        
#         self.accumulator_label = tk.Label(self.status_container, text=f"Accumulator: {self.vm.accumulator}")
#         self.accumulator_label.pack(anchor=tk.NW)

#         self.pc_label = tk.Label(self.status_container, text=f"Program Counter: {self.vm.program_counter}")
#         self.pc_label.pack()
    
#     def populate_console_container(self):
#         console_header = VMHeader(self.console_container, text="Console")
#         console_header.pack(anchor=tk.W)

#         self.textbox = tk.Text(self.console_container, height=18, width=40)
#         self.textbox.pack()

#         self.textbox.bind("<Return>", self.on_enter_pressed)

#         enter_button = tk.Button(self.console_container, text="Enter", command=self.on_enter_pressed)
#         enter_button.pack(pady=5)

#     def on_enter_pressed(self, event=None):
#         command = self.textbox.get("1.0", "end-1c")
#         self.textbox.delete("1.0", "end")
#         self.input_redirector.set_input(command + "\n")

#     def select_file(self):
#         file_path = filedialog.askopenfilename()
#         if file_path == () or file_path == "":             
#             return
#         try:
#             self.pl.load(self.vm, file_path)
#             self.update_screen()
#             messagebox.showinfo("Success!", "Your program is loaded and ready to run")
#         except Exception as details:
#             messagebox.showerror("Invalid File", details) 
    
#     def update_screen(self):
#         for item in self.memory_tree.get_children():
#             self.memory_tree.delete(item)

#         for i, value in enumerate(self.vm.memory):
#             address = f"{i:02d}"
#             self.memory_tree.insert("", "end", values=(address, value))
#         self.style_memory_tree()
        
#         self.accumulator_label.config(text=f"Accumulator: {self.vm.accumulator}")
#         self.pc_label.config(text=f"Program Counter: {self.vm.program_counter}")

#     def run_from_start(self):
#         def run_program():
#             self.vm.program_counter = 0
#             for _ in self.vm.run_by_step():
#                 self.update_screen()
#             self.update_screen()

#         threading.Thread(target=run_program).start()

# class TextRedirector:
#     def __init__(self, widget, tag="stdout"):
#         self.widget = widget
#         self.tag = tag

#     def write(self, string):
#         self.widget.configure(state="normal")
#         self.widget.insert("end", string, (self.tag,))
#         self.widget.configure(state="disabled")
#         self.widget.update()

#     def flush(self):
#         pass

# class InputRedirector:
#     def __init__(self, app):
#         self.app = app
#         self.input_ready = threading.Event()
#         self.input_value = None

#     def set_input(self, value):
#         self.input_value = value
#         self.input_ready.set()

#     def readline(self):
#         self.input_ready.wait()
#         self.input_ready.clear()
#         return self.input_value

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VMApp(root)
#     root.mainloop()


import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from vm import VM, ProgramLoader
import sys
import threading

class VMHeader(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, font=("Helvetica", 16, "bold"), pady=10)

class VMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VM")
        self.vm = VM()
        self.pl = ProgramLoader()

        self.container = tk.Frame(self.root)
        self.container.pack(pady=50, padx=20)
        
        self.memory_container = tk.Frame(self.container)
        self.memory_container.pack(side=tk.LEFT, padx=20, pady=30)

        status_console_container = tk.Frame(self.container)
        status_console_container.pack(padx=20, pady=30)

        self.status_container = tk.Frame(status_console_container)
        self.status_container.pack(anchor=tk.NW)

        self.console_container = tk.Frame(status_console_container)
        self.console_container.pack(pady=30)

        self.populate_memory_container()
        self.populate_accumulator_container()
        self.populate_console_container()
        self.update_screen()

        # Redirect stdout and stdin to the text box
        sys.stdout = TextRedirector(self.textbox, "stdout")
        self.input_redirector = InputRedirector(self)
        sys.stdin = self.input_redirector

    def populate_memory_container(self):
        memory_title = VMHeader(self.memory_container, text="Memory")
        memory_title.pack(side=tk.TOP, anchor=tk.W)

        memory_frame = tk.Frame(self.memory_container)
        memory_frame.pack()

        self.memory_tree = ttk.Treeview(
            memory_frame,
            columns=("Address", "Value"),
            show="headings",
            height=20
        )
        self.memory_tree.heading("Address", text="Address")
        self.memory_tree.heading("Value", text="Value")

        self.memory_tree.column("Address", anchor=tk.CENTER, width=180)
        self.memory_tree.column("Value", anchor=tk.CENTER, width=180)
        
        self.memory_tree.pack()

        select_file_button = tk.Button(self.memory_container, text="Import File", command=self.select_file)
        select_file_button.pack(pady=5)

        run_button = tk.Button(self.memory_container, text="Run Program", command=self.run_from_start)
        run_button.pack()

    def style_memory_tree(self):
        self.memory_tree.tag_configure('evenrow', background='lightgrey')
        for index, row in enumerate(self.memory_tree.get_children()):
            if index % 2 == 0:
                self.memory_tree.item(row, tags=('evenrow',))

    def populate_accumulator_container(self):
        VMHeader(self.status_container, text="Status").pack(anchor=tk.NW)
        
        self.accumulator_label = tk.Label(self.status_container, text=f"Accumulator: {self.vm.accumulator}")
        self.accumulator_label.pack(anchor=tk.NW)

        self.pc_label = tk.Label(self.status_container, text=f"Program Counter: {self.vm.program_counter}")
        self.pc_label.pack()
    
    def populate_console_container(self):
        console_header = VMHeader(self.console_container, text="Console")
        console_header.pack(anchor=tk.W)

        self.textbox = tk.Text(self.console_container, height=18, width=40)
        self.textbox.pack()

        self.textbox.bind("<Return>", self.on_enter_pressed)

        enter_button = tk.Button(self.console_container, text="Enter", command=self.on_enter_pressed)
        enter_button.pack(pady=5)

    def on_enter_pressed(self, event=None):
        command = self.textbox.get("end-1c linestart", "end-1c lineend")
        # self.textbox.delete("1.0", "end")
        self.input_redirector.set_input(command)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path == () or file_path == "":             
            return
        try:
            self.pl.load(self.vm, file_path)
            messagebox.showinfo("Success!", "Your program is loaded and ready to run")
        except Exception as details:
            messagebox.showerror("Invalid File", details) 
    
    def update_screen(self):
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)

        for i, value in enumerate(self.vm.memory):
            address = f"{i:02d}"
            self.memory_tree.insert("", "end", values=(address, value))
        self.style_memory_tree()
        
        self.accumulator_label.config(text=f"Accumulator: {self.vm.accumulator}")
        self.pc_label.config(text=f"Program Counter: {self.vm.program_counter}")

    def run_from_start(self):
        def run_program():
            self.vm.program_counter = 0
            self.vm.accumulator = 0
            self.textbox.delete("1.0", "end")
            self.update_screen()
            for _ in self.vm.run_by_step():
                self.update_screen()
            self.update_screen()

        threading.Thread(target=run_program).start()

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, string):
        self.widget.configure(state="normal")
        self.widget.insert("end", string, (self.tag,))
        # self.widget.configure(state="disabled")
        self.widget.update()

    def flush(self):
        pass

class InputRedirector:
    def __init__(self, app):
        self.app = app
        self.input_ready = threading.Event()
        self.input_value = None

    def set_input(self, value):
        self.input_value = value
        self.input_ready.set()

    def readline(self):
        self.input_ready.wait()
        self.input_ready.clear()
        return self.input_value

if __name__ == "__main__":
    root = tk.Tk()
    app = VMApp(root)
    root.mainloop()
