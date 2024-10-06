from TkinterExtended.exceptions import WidgetAlreadyInStackError, NotInStackError, DuplicateNameError

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

    def add_widget(self, widget: BASECLASS, name: str | None = None, index: int | None = None) -> None: # type: ignore
        """
        adds a widget to the stack
        """
        for child in self.children_list:
            if child["widget"] == widget:
                raise WidgetAlreadyInStackError(widget)
                
        if name is not None:
            for child in self.children_list:
                if child["name"] == name:
                    widget = child["widget"]
                    name = child["name"]
                    raise DuplicateNameError(widget, name)

        widget.grid(row = 0, column = 0, sticky = "nsew")
        widget.grid_remove()

        if index is not None:
            self.children_list.insert(index, {"widget": widget, "name": name})
        else:
            self.children_list.append({"widget": widget, "name": name})

        if self.visible_child is None:  
            self.set_visible_child(widget)

    def remove_widget(self, widget_or_identifier: BASECLASS | str | int) -> None: # type: ignore
        """
        removes a widget from the stack
        """
        if isinstance(widget_or_identifier, BASECLASS):
            self._remove_widget_by_object(widget_or_identifier)
            
        if isinstance(widget_or_identifier, str):
            self._remove_widget_by_name(widget_or_identifier)

        if isinstance(widget_or_identifier, int):
            self._remove_widget_by_index(widget_or_identifier)

    def set_visible_child(self, widget_or_identifier: BASECLASS | str | int) -> None: # type: ignore
        """
        sets visible the widget.
        """
        if isinstance(widget_or_identifier, BASECLASS):
            self._set_visible_child_by_object(widget_or_identifier)
            
        if isinstance(widget_or_identifier, str):
            self._set_visible_child_by_name(widget_or_identifier)

        if isinstance(widget_or_identifier, int):
            self._set_visible_child_by_index(widget_or_identifier)

    def get_visible_child(self) -> type(BASECLASS) | None: # type: ignore
        """
        gets the currently visible widget in the stack.
        """ 
        return self.visible_child
    
    def get_stack_size(self) -> int:
        """
        gets the size of the stack.
        """
        return len(self.children_list)

    def is_widget_in_stack(self, widget) -> bool:
        """
        checks if a widget is in the stack.
        """
        for child in self.children_list:
            if child["widget"] == widget:
                return True
        return False

    def get_stack_state(self) -> int:
        """
        gets the index of the current widget set to be visible.
        allows user to save the state of the stack.
        """
        return self.children_list.index(self.visible_child)

    def load_stack_state(self, index) -> None:
        """
        sets the widget with the given index to be visible.
        allows the user to load a saved state of the stack.
        """
        self._set_visible_child_by_index(index)

    def clear_stack(self) -> None:
        """
        removes all widgets from the stack
        """
        for child in self.children_list:
            self.remove_widget(child["widget"])
    
    def show_next(self) -> None:
        """
        Shows the next widget in the stack by index
        """
        current_index = self.children_list.index(self.visible_child)
        if current_index < len(self.children_list) -1:
            self._set_visible_child_by_index(current_index+1)
        else:
            self._set_visible_child_by_index(0)

    def show_previous(self) -> None:
        """
        Shows the previous widget in the stack by index.
        """
        current_index = self.children_list.index(self.visible_child)
        if current_index > 0:
            self._set_visible_child_by_index(current_index-1)
        else:
            self._set_visible_child_by_index(-1)

    def _remove_widget_by_object(self, widget):
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

    def _remove_widget_by_name(self, name):
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

    def _remove_widget_by_index(self, index):
        child = self.children_list[index]
        widget = child["widget"]
        self.children_list.remove(widget)

        if widget == self.visible_child:
            if self.children_list:
                self.set_visible_child(self.children_list[0]) 
            else:
                self.visible_child = None

    def _set_visible_child_by_object(self, widget):
        if any(child["widget"] == widget for child in self.children_list):
            if self.visible_child:
                self.visible_child.grid_remove()

            widget.grid()
            self.visible_child = widget
        else:
            raise NotInStackError(widget)

    def _set_visible_child_by_name(self, name):
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

    def _set_visible_child_by_index(self, index):
        child = self.children_list[index]

        if self.visible_child:
            self.visible_child.grid_remove()  # Hide the current visible widget

        widget = child["widget"]
        widget.grid()  # Show the widget associated with the name
        self.visible_child = widget