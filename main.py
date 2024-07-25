import customtkinter as ctk
from gui import VMApp
from config import WINDOW_WIDTH, WINDOW_HEIGHT, THEME_FILE, DEFAULT_APPEARANCE_MODE
from json.decoder import JSONDecodeError

class TabbedVMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed VM Simulator")
        self.setup_window()
        self.setup_theme()

        # Create a notebook (tabbed interface)
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Add initial tab
        self.add_tab()

        # Add "+" button for new tabs
        self.add_tab_button = ctk.CTkButton(self.root, text="+", command=self.add_tab, width=30)
        self.add_tab_button.pack(side="top", anchor="ne", padx=5, pady=5)

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
        tab_name = f"VM {len(self.notebook._tab_dict) + 1}"
        new_tab = self.notebook.add(tab_name)
        
        # Create a frame to hold the VMApp instance
        frame = ctk.CTkFrame(new_tab)
        frame.pack(expand=True, fill="both")

        # Create a new VMApp instance inside the frame
        VMApp(frame)

def main():
    root = ctk.CTk()
    TabbedVMApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()