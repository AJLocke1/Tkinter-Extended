try:
    import customtkinter as ctk
    STACKBASE = ctk.CTkFrame
    BASECLASS = ctk.CTkBaseClass
except ModuleNotFoundError:
    import tkinter as tk
    STACKBASE = tk.Frame
    BASECLASS = tk.Widget

class Stack(STACKBASE):
    """
    A stack wiget based on the c++ gtkmm4 widget of the same name.
    This widgetis ideal for setting up multi page applications.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.children_list = []
        self.visible_child = None

    def add_widget(self, widget: BASECLASS, name: str | None = None) -> None: # type: ignore
        """
        adds a widget to the stack
        """
        if name is not None:
            for child in self.children_list:
                if child["name"] == name:
                    widget = child["widget"]
                    name = child["name"]
                    raise DuplicateNameError(widget, name)

        widget.grid(row = 0, column = 0, sticky = "nsew")
        widget.grid_remove()
        self.children_list.append({"widget": widget, "name": name})

        if self.visible_child is None:  
            self.set_visible_child(widget)

    def remove_widget(self, widget_or_identifier: BASECLASS | str) -> None: # type: ignore
        """
        removes a widget from the stack
        """
        if isinstance(widget_or_identifier, BASECLASS):
            widget = widget_or_identifier
            if any(child["widget"] == widget for child in self.children_list):
                widget.grid_forget()
                self.children_list.remove(widget)

                if widget == self.visible_child:
                    if self.children_list:
                        self.set_visible_child(self.children_list[0]) 
                    else:
                        self.visible_child = None
            else:
                raise NotInStackError(widget)
        else:
            name = widget_or_identifier
            if any(child["name"] == name for child in self.children_list):
                for child in self.children_list:
                    if child["name"] == name:
                        widget = child["widget"]
                        widget.grid_forget()
                        self.children_list.remove(widget)

                        if widget == self.visible_child:
                            if self.children_list:
                                self.set_visible_child(self.children_list[0]) 
                            else:
                                self.visible_child = None
            else:
                raise NotInStackError(widget)

    def set_visible_child(self, widget_or_identifier: BASECLASS | str) -> None: # type: ignore
        """
        sets visible the widget.
        """
        if isinstance(widget_or_identifier, BASECLASS):
            widget = widget_or_identifier
            if any(child["widget"] == widget for child in self.children_list):
                if self.visible_child:
                    self.visible_child.grid_remove()

                widget.grid()
                self.visible_child = widget
            else:
                raise NotInStackError(widget)
        if isinstance(widget_or_identifier, str):
            name = widget_or_identifier
            if any(child["name"] == name for child in self.children_list):
                for child in self.children_list:
                    if child["name"] == name:
                        if self.visible_child:
                            self.visible_child.grid_remove()  # Hide the current visible widget

                        widget = child["widget"]
                        widget.grid()  # Show the widget associated with the name
                        self.visible_child = widget
            else:
                raise NotInStackError(widget)

    def get_visible_child(self) -> type(BASECLASS) | None: # type: ignore
        """
        gets the currently visible widget in the stack.
        """ 
        return self.visible_child
    
class NotInStackError(Exception):
    def __init__(self, widget):
        self.widget = widget
        self.message = f"Widget: {widget} is not appart of the stack"
    def __str__(self):
        return self.message
    
class DuplicateNameError(Exception):
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name
        self.message = f"Widget in stack: {widget} already has the name {name}. please choose a unique name"
    def __str__(self):
        return self.message
