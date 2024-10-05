class DuplicateNameError(Exception):
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name
        self.message = f"Widget in stack: {widget} already has the name {name}. please choose a unique name"
    def __str__(self):
        return self.message