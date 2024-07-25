import customtkinter as ctk
from gui import VMApp
from config import WINDOW_WIDTH, WINDOW_HEIGHT, THEME_FILE, DEFAULT_APPEARANCE_MODE
from json.decoder import JSONDecodeError

class CustomTabview(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tab_apps = {}

    def add(self, name):
        new_tab = super().add(name)
        vm_app = VMApp(new_tab, self)
        self.tab_apps[name] = vm_app
        return new_tab

    def set(self, name):
        current_name = self.get()
        if current_name in self.tab_apps and self.tab_apps[current_name].is_running:
            return  # Prevent tab change if current program is running
        super().set(name)

class TabbedVMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed VM Simulator")
        self.setup_window()
        self.setup_theme()

        self.notebook = CustomTabview(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.add_tab_button = ctk.CTkButton(self.root, text="+", command=self.add_tab, width=30)
        self.add_tab_button.pack(side="top", anchor="ne", padx=5, pady=5)

        self.add_tab()  # Add initial tab

    def setup_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - WINDOW_WIDTH/2)
        center_y = int(screen_height/2 - WINDOW_HEIGHT/2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

    def setup_theme(self):
        try:
            ctk.set_default_color_theme(THEME_FILE)
            ctk.set_appearance_mode(DEFAULT_APPEARANCE_MODE)
        except JSONDecodeError:
            print("Error loading theme file. Using default theme.")

    def add_tab(self):
        if len(self.notebook.tab_apps) < 15:
            tab_name = f"VM {len(self.notebook.tab_apps) + 1}"
            self.notebook.add(tab_name)

def main():
    root = ctk.CTk()
    TabbedVMApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()