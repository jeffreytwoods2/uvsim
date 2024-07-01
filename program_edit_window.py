import tkinter as tk
from tkinter import messagebox

class ProgramEditor:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.root = self.parent_app.root
        self.memory = []
    
    def calculate_window_placement(self):
        self.root.update_idletasks() 
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()

        new_width = main_width // 2
        new_height = main_height
        
        new_x = main_x + (main_width - new_width) // 2
        new_y = main_y + (main_height - new_height) // 2

        return f"{new_width}x{new_height}+{new_x}+{new_y}"

    def open(self):
        def process_text():
            text_content = self.text_area.get("1.0", tk.END).strip()
            try:
                self.parent_app.pl.load_string(self.parent_app.vm, text_content)
                on_close()
            except Exception as details:
                messagebox.showerror("Invalid Program", details, parent=program_edit_window)
        
        def on_close():
            text_content = self.text_area.get("1.0", tk.END).strip()
            self.memory = [line for line in text_content.split("\n")]
            self.parent_app.update_screen()
            program_edit_window.destroy()

        program_edit_window = tk.Toplevel(self.root)
        program_edit_window.title("Program Editor")
        program_edit_window.protocol("WM_DELETE_WINDOW", on_close)
        
        program_edit_window.geometry(self.calculate_window_placement())

        self.text_area = tk.Text(program_edit_window, height=35, width=30)
        self.text_area.pack(pady=5)

        for word in self.memory:
            self.text_area.insert(tk.END, f"{word}\n")
        
        process_button = tk.Button(program_edit_window, text="Process", command=process_text)
        process_button.pack(pady=5)