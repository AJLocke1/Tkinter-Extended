# TkinterExtended/exceptions/__init__.py

from .duplicate_name_error import DuplicateNameError
from .not_in_stack_error import NotInStackError
from .widget_already_in_stack_error import WidgetAlreadyInStackError

__all__ = ["DuplicateNameError", "NotInStackError", "WidgetAlreadyInStackError"]
