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
