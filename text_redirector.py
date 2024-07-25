class TextRedirector:
    def __init__(self, string_var, app, tag="stdout"):
        self.string_var = string_var
        self.app = app
        self.tag = tag

    def write(self, string):
        current_value = self.string_var.get()
        self.string_var.set(current_value + string)
        if self.app.waiting_for_input:
            self.app.display_prompt()

    def flush(self):
        pass

# Class to handle input redirection from the GUI console
class InputRedirector:
    def __init__(self, input_queue, app):
        self.input_queue = input_queue
        self.app = app

    def readline(self, prompt=''):
        self.app.waiting_for_input = True
        if prompt:
            self.app.output_redirector.write(prompt)
        self.app.display_prompt()
        result = self.input_queue.get() + '\n'
        self.app.waiting_for_input = False
        return result