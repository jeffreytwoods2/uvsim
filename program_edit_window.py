import customtkinter as ctk
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

        new_width = 450
        new_height = 550
        
        new_x = main_x + (main_width - new_width) // 2
        new_y = main_y + (main_height - new_height) // 2

        return f"{new_width}x{new_height}+{new_x}+{new_y}"

    def open(self):
        self.program_edit_window = ctk.CTkToplevel(self.root)
        self.program_edit_window.title("Program Editor")
        self.program_edit_window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.program_edit_window.geometry(self.calculate_window_placement())

        # Create main frame
        main_frame = ctk.CTkFrame(self.program_edit_window)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Add "Program Editor" header
        header = ctk.CTkLabel(main_frame, text="Program Editor", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=(10))

        # Text area
        self.text_area = ctk.CTkTextbox(main_frame, height=400, width=300)
        self.text_area.pack(pady=10)

        for word in self.memory:
            self.text_area.insert("end", f"{word}\n")
        
        # Process button
        process_button = ctk.CTkButton(main_frame, text="Process", command=self.process_text)
        process_button.pack(pady=5)
        # Make sure the window is on top
        self.program_edit_window.attributes('-topmost', True)
         
    def process_text(self):
        try:
            self.parent_app.pl.load_string(self.parent_app.vm, self.get_file_content())
            self.save_memory()
            self.on_close()
        except Exception as details:
            messagebox.showerror("Invalid Program", details, parent=self.program_edit_window)
        
    def on_close(self):
        self.program_edit_window.destroy()
        self.parent_app.clear_all_fields()
        self.parent_app.update_screen()
    
    def save_memory(self):
        self.memory = [line for line in self.get_file_content().split("\n")]
    
    def get_file_content(self):
        return self.text_area.get("1.0", "end").strip()
