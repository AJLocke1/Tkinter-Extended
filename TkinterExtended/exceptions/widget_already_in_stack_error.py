class WidgetAlreadyInStackError(Exception):
    def __init__(self, widget):
        self.widget = widget
        self.message = f"Widget: {widget} is already appart of the stack"
    def __str__(self):
        return self.message