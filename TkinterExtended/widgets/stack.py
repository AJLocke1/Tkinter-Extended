from TkinterExtended.exceptions import WidgetAlreadyInStackError, NotInStackError, DuplicateNameError
import inspect
import warnings

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
    The widget automatically takes the colour of the widget beneath it.

    Args:
        STACKBASE (Frame): A container widget

    Attributes:
        children_list (array): an array of all the widgets in the stack.
        visible_child (Widget): the widget component of the child currently visible.
        children_expandable (bool): if the widgets in the stack can expand.
    """
    def __init__(self, *args, children_expandable = False, **kwargs):
        super().__init__(*args, bg_color = "transparent", fg_color = "transparent", **kwargs)

        self.children_list: list = [] #cant be a set as it needs to be ordered.
        self.visible_child: BASECLASS = None # type: ignore
        self.children_expandable: bool = children_expandable

        self._on_add_widget_callbacks: set[callable] = set() 
        self._on_remove_widget_callbacks: set[callable] = set()
        self._on_change_visible_widget_callbacks: set[callable] = set()

        if self.children_expandable:
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

    def add_widget(self, widget: BASECLASS, name: str | None = None, index: int | None = None, expandable: bool | None = None) -> None: # type: ignore
        """
        Based on the arguments provided it calls the necessary private add method to add a widget to the stack.

        Args:
            widget (BASECLASS): Any tkinter widget to add to the stack
            name (str | None, optional): An optional identifier for the widget. Defaults to None.
            index (int | None, optional): An optional index to add the widget to a certain point in 
                the stack. Defaults to None.
            expandable(bool | None, optional): An optional bool to allow a widget to expand or not, 
                defaults to the children_expandable attribute of the stack.

        Raises:
            WidgetAlreadyInStackError: Throws an error if the widget being added is already in the stack.
            DuplicateNameError: Throws an error if the optional identifier being specified is already in use 
                for this stack.
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

        if expandable is None:
            expandable = self.children_expandable
        
        if expandable:
            widget.grid(row = 0, column = 0, sticky = "nsew")
        else:
            widget.grid(row = 0, column = 0)

        widget.grid_remove()

        if index is not None:
            self.children_list.insert(index, {"widget": widget, "name": name})
        else:
            self.children_list.append({"widget": widget, "name": name})

        if self.visible_child is None:  
            self.set_visible_child(widget)
        
        self._trigger_event_callbacks(event = "add_widget", widget = widget)

    def remove_widget(self, widget_or_identifier: BASECLASS | str | int) -> None: # type: ignore
        """
            Based on the arguments provided it calls the necessary private remove method to remove a widget to 
            the stack. Valid options are the widget object to be removed, the name of the widget, or the 
            index of the widget in the stack.

        Args:
            widget_or_identifier (BASECLASS | str | int): any identifier used to remove a widget.
        """
        if isinstance(widget_or_identifier, BASECLASS):
            self._remove_widget_by_object(widget_or_identifier)
            
        if isinstance(widget_or_identifier, str):
            self._remove_widget_by_name(widget_or_identifier)

        if isinstance(widget_or_identifier, int):
            self._remove_widget_by_index(widget_or_identifier)

        self._trigger_event_callbacks(event = "remove_widget", widget = widget_or_identifier)

    def set_visible_child(self, widget_or_identifier: BASECLASS | str | int) -> None: # type: ignore
        """
            Based on the arguments provided it calls the necessary private set visible method to set a widget 
            to be visible. Valid options are the widget object to be removed, the name of the widget, or the 
            index of the widget in the stack.

        Args:
            widget_or_identifier (BASECLASS | str | int): any identifier used to set the widget as visible.
        """
        if isinstance(widget_or_identifier, BASECLASS):
            self._set_visible_child_by_object(widget_or_identifier)
            
        if isinstance(widget_or_identifier, str):
            self._set_visible_child_by_name(widget_or_identifier)

        if isinstance(widget_or_identifier, int):
            self._set_visible_child_by_index(widget_or_identifier)
        
        self._trigger_event_callbacks(event = "change_visible_widget", widget = widget_or_identifier)

    def get_visible_child(self) -> BASECLASS | None: # type: ignore
        """
        gets the currently visible widget.

        Returns:
            Widget | none: The currently visible widget.
        """
        return self.visible_child
    
    def get_stack_size(self) -> int:
        """
        gets the size of the stack.

        Returns:
            int: the size of the stack.
        """
        return len(self.children_list)

    def is_widget_in_stack(self, widget: BASECLASS) -> bool: # type: ignore
        """
        checks if a widget is in the stack.

        Args:
            widget (BASECLASS): the widget to check.

        Returns:
            bool: if the widget is in the stack.
        """
        for child in self.children_list:
            if child["widget"] == widget:
                return True
        return False

    def get_stack_state(self) -> int:
        """
        gets the index of the current widget set to be visible.
        allows user to save the state of the stack.

        Returns:
            int: the index of the currently visible widget.
        """
        return self.children_list.index(self.visible_child)

    def load_stack_state(self, index: int) -> None:
        """
        sets the widget with the given index to be visible.
        allows the user to load a saved state of the stack.

        Args:
            index (int): the index of the widget to set visible.
        """
        self._set_visible_child_by_index(index)

    def clear_stack(self) -> None:
        """
        removes all widgets from the stack
        """
        for child in self.children_list.copy():
            self.remove_widget(child["widget"])
    
    def show_next(self) -> None:
        """
        Shows the next widget in the stack by index
        """
        for child in self.children_list:
            if child["widget"] == self.visible_child:
                current_index = self.children_list.index(child)
        if current_index < len(self.children_list) -1:
            self.set_visible_child(current_index+1)
        else:
            self.set_visible_child(0)

    def show_previous(self) -> None:
        """
        Shows the previous widget in the stack by index.
        """
        for child in self.children_list:
            if child["widget"] == self.visible_child:
                current_index = self.children_list.index(child)
        if current_index > 0:
            self.set_visible_child(current_index-1)
        else:
            self.set_visible_child(-1)

    def _remove_widget_by_object(self, widget: BASECLASS): # type: ignore
        """
        the private method for removing a widget by its object.

        Args:
            widget (BASECLASS): the object to remove.

        Raises:
            NotInStackError: the widget is not in the stack.
        """
        if any(child["widget"] == widget for child in self.children_list):
            for child in self.children_list:
                if child["widget"] == widget:
                    widget = child["widget"]
                    widget.grid_forget()
                    self.children_list.remove(child)

            if widget == self.visible_child:
                if self.children_list:
                    self.set_visible_child(self.children_list[0]) 
                else:
                    self.visible_child = None
        else:
            raise NotInStackError(widget)

    def _remove_widget_by_name(self, name: str):
        """
        the private method for removing a widget by its name

        Args:
            name (str): the name of the widget given to the stack

        Raises:
            NotInStackError: the widget is not in the stack.
        """
        if any(child["name"] == name for child in self.children_list):
            for child in self.children_list:
                if child["name"] == name:
                    widget = child["widget"]
                    widget.grid_forget()
                    self.children_list.remove(child)

                    if widget == self.visible_child:
                        if self.children_list:
                            self.set_visible_child(self.children_list[0]) 
                        else:
                            self.visible_child = None
        else:
            raise NotInStackError(name)

    def _remove_widget_by_index(self, index: int):
        """
        the private method for removing a widget by its index

        Args:
            index (int): the index of the widget to remove.

        Raises:
            IndexError: index out of range.
        """
        if index < 0 or index > len(self.children_list)-1:
            raise IndexError(f"Index {index} is out of range.")
    
        child = self.children_list[index]
        widget = child["widget"]
        self.children_list.remove(child)

        if widget == self.visible_child:
            if self.children_list:
                self.set_visible_child(self.children_list[0]) 
            else:
                self.visible_child = None

    def _set_visible_child_by_object(self, widget: BASECLASS): #type: ignore
        """
        the private method for making a widget visible by its object.

        Args:
            widget (BASECLASS): the object to remove.

        Raises:
            NotInStackError: The widget is not in the stack.
        """
        if any(child["widget"] == widget for child in self.children_list):
            if self.visible_child:
                self.visible_child.grid_remove()

            widget.grid()
            self.visible_child = widget
        else:
            raise NotInStackError(widget)

    def _set_visible_child_by_name(self, name: str):
        """
        the private method for making a widget visible by its name

        Args:
            name (str): the name of the widget given to the stack

        Raises:
            NotInStackError: The widget is not in the stack.
        """
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

    def _set_visible_child_by_index(self, index: int):
        """
        the private method for making a widget visible by its index.

        Args:
            index (int): the index of the widget in the stack

        Raises:
            IndexError: index out of range.
        """
        if (index < 0 or index > len(self.children_list)-1) and index != -1:
            raise IndexError(f"Index {index} is out of range.")
        
        child = self.children_list[index]

        if self.visible_child:
            self.visible_child.grid_remove()  # Hide the current visible widget

        widget = child["widget"]
        widget.grid()  # Show the widget associated with the name
        self.visible_child = widget

    def add_callback_function(self, event: str, callback_function: callable) -> None: 
        """
        Adds a callback function for the specified event. All callback function will automatically be passed
        the event and widget effected in the key word arguments **kwargs. if this is not present in your funtion
        these arguments will be discarded using a try-catch.

        Args:
            event (str): events are, add_widget, remove_widget and change_visible_widget.
            callback_function (callable): the callback function to be added.

        Raises:
            TypeError: an error if the callback_function passed is not callable.
            ValueError: if the event is invalid.
        """
        if callable(callback_function): 

            signature = inspect.signature(callback_function)
            parameters = signature.parameters

            if ("event" not in parameters or "widget" not in parameters) and "**kwargs" not in parameters:
                warnings.warn(f"Warning: The callback function {callback_function.__name__} does not accept 'event' "
                                "and/or 'widget' parameters. These will not be passed to the function.")
        
            match event:
                case "add_widget":
                    self._on_add_widget_callbacks.add(callback_function)
                case "remove_widget":
                    self._on_remove_widget_callbacks.add(callback_function)
                case "change_visible_widget":
                    self._on_change_visible_widget_callbacks.add(callback_function)
                case _:
                    raise ValueError(f"{event} is an invalid event. valid events: add_widget, remove_widget, and change_visible_widget")
        else:
            raise TypeError(f"Object {callback_function} is not callable")
        
    def remove_callback_function(self, event: str, callback_function: callable) -> None: 
        """
        removes a callback function for the specified event.

        Args:
            event (str): events are, add_widget, remove_widget and change_visible_widget.
            callback_function (callable): the callback function to be removed.

        Raises:
            TypeError: an error if the callback_function passed is not callable.
            ValueError: if the event is invalid.
        """
        if callable(callback_function): 
            match event:
                case "add_widget":
                    self._on_add_widget_callbacks.discard(callback_function)
                case "remove_widget":
                    self._on_remove_widget_callbacks.discard(callback_function)
                case "change_visible_widget":
                    self._on_change_visible_widget_callbacks.discard(callback_function)
                case _:
                    raise ValueError(f"{event} is an invalid event. valid events: add_widget, remove_widget, and change_visible_widget")
        else:
            raise TypeError(f"Object {callback_function} is not callable")
    
    def get_callback_functions(self, event: str) -> set[callable]:
        """
        gets the specified set of callback functions relating to the event.

        Args:
            event (str): events are, add_widget, remove_widget and change_visible_widget.

        Raises:
            ValueError: if the event is invalid.

        Returns:
            set[callable]: the set of callback functions.
        """
        match event:
            case "add_widget":
                return self._on_add_widget_callbacks
            case "remove_widget":
                return self._on_remove_widget_callbacks
            case "change_visible_widget":
                return self._on_change_visible_widget_callbacks
            case _:
                raise ValueError(f"{event} is an invalid event. valid events: add_widget, remove_widget, and change_visible_widget")
        
    def _trigger_event_callbacks(self, event: str, **kwargs):
        """
        private method that calls the callback functions when an event happens.

        Args:
            event (str): events are, add_widget, remove_widget and change_visible_widget.
            **kwargs: Keyword arguments passed to the callback fucntions.

        Raises:
            TypeError: if the users function doesnt accept given keyword arguments it will recall it 
            without them.

        """
        match event:
            case "add_widget":
                for callback in self._on_add_widget_callbacks:
                    try:
                        callback(**kwargs)
                    except TypeError:
                        callback()
            case "remove_widget":
                for callback in self._on_remove_widget_callbacks:
                    try:
                        callback(**kwargs)
                    except TypeError:
                        callback()
            case "change_visible_widget":
                for callback in self._on_change_visible_widget_callbacks:
                    try:
                        callback(**kwargs)
                    except TypeError:
                        callback()

   