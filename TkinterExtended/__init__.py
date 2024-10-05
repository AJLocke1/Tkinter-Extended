from .widgets import Stack

from .exceptions import DuplicateNameError, NotInStackError, WidgetAlreadyInStackError


__all__ = [
    "Stack",
    "DuplicateNameError",
    "NotInStackError",
    "WidgetAlreadyInStackError"
]

#Package metadata
__version__ = "0.0.1"
__author__ = "Your Name"
__description__ = "A Tkinter extension for creating stack-like widgets and managing exceptions."
