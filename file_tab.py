import customtkinter as ctk
from vm import VM, ProgramLoader
from program_edit_window import ProgramEditor

class FileTab:
    def __init__(self, parent_notebook, file_path=None):
        self.parent_notebook = parent_notebook
        self.file_path = file_path
        self.vm = VM()
        self.pl = ProgramLoader()
        self.program_editor = ProgramEditor(self)
        
        self.frame = ctk.CTkFrame(self.parent_notebook)
        self.text_area = ctk.CTkTextbox(self.frame, height=400, width=300)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as file:
            content = file.read()
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('1.0', content)
        self.pl.load(self.vm, file_path)
    
    def get_content(self):
        return self.text_area.get('1.0', 'end-1c')
    
    def set_content(self, content):
        self.text_area.delete('1.0', 'end')
        self.text_area.insert('1.0', content)
    
    def run_program(self):
        content = self.get_content()
        self.pl.load_string(self.vm, content)
        self.vm.run