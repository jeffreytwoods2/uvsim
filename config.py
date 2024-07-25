# VM Configuration
MEMORY_LENGTH = 250
WORD_LENGTH = 6

# GUI Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700

# Theme Configuration
THEME_FILE = "theme.json"
DEFAULT_APPEARANCE_MODE = "dark"

# File types for open/save dialogs
FILE_TYPES = [("Text files", "*.txt"), ("All files", "*.*")]

# Error messages
ERR_INVALID_WORD = "Invalid word. Please enter a {}-digit word between -{} and {}."
ERR_PROGRAM_TOO_LARGE = "Program is larger than available memory."
ERR_NO_HALT_INSTRUCTION = "Program does not contain HALT instruction."
ERR_INVALID_MEMORY_ADDRESS = "Invalid memory address: {}"
ERR_INVALID_OPCODE = "Invalid opcode: {}"
ERR_EXECUTION = "An error occurred while running the program: {}"
ERR_FILE_LOAD = "Failed to load file: {}"
ERR_FILE_SAVE = "Failed to save file: {}"
ERR_NO_FILE_PATH = "No file path specified"
ERR_THEME_LOAD = "Failed to load theme: {}"