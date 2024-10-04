from typing import Tuple
import customtkinter as ctk

class App(ctk.CTk):
    """
    The custom application class for use of pages. 

    Attributes:
    -   page_list(list): A List of all the page objects created

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_list = []
        self.navbar_image = None
        self.navbar_title = None

        self.theme_highlight_color = ['gray81', 'gray20']
        self.theme_dampend_highlight_color = ['#36719F', '#144870']

    def add_page(self, page):
        self.page_list.append(page)
        self.on_page_list_change()

    def on_page_list_change(self):
        for page in self.page_list:
            page.refresh_navbar()

    def show_page(self, identifier: str):
        for page in self.page_list:
            for button in page.navbar.buttons:
                if getattr(button, "_text") == page.navbar_name:
                    button.configure(bg_color = self.theme_dampend_highlight_color)
                button.configure(bg_color = self.theme_highlight_color)
            if page.identifier == identifier:
                page.lift()

class Custom_Page():
    """
    A better option for applications with multiple pages. Must use the grid manager.
    initialize the navbar in the application class after all pages are initialized.
    """
    def __init__(self, *args, identifier: str, has_navbar: bool, has_sidebar: bool, navbar_name: str = None, expand_navbar = True, centre_navbar = True, autogen_sidebar = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = identifier
        self.has_navbar = has_navbar
        self.has_sidebar = has_sidebar
        self.navbar_name = navbar_name if navbar_name else identifier
        self.expand_navbar = expand_navbar
        self.centre_navbar = centre_navbar
        self.navbar = None

        self.column_offset = 1 if self.has_sidebar else 0
        self.row_offset = 1 if self.has_navbar else 0

        self.winfo_toplevel().add_page(self)

        self.place(relx=0.5, rely=0.5, anchor="center" ,relwidth = 1, relheight = 1)
        if has_navbar:
            self.grid_columnconfigure(0, weight = 1)
            self.refresh_navbar()
    
    def initialize_sidebar(self, sub_pages: list):
        pass

    def add_widget(self, widget, **kwargs):
        if widget.master != self:
            raise("Widget does not belong to this page")

        row = kwargs.pop("row") + self.row_offset
        column = kwargs.pop("column") + self.column_offset
        widget.grid(row = row, column = column, **kwargs)
        self.refresh_navbar()

    def remove_widget(self, widget):
        if widget.master != self:
            raise("Widget does not belong to this page")
        widget.grid_remove()

    def refresh_navbar(self):
        if self.has_navbar:
            if not self.navbar:
                self.navbar = Navbar(self, self.winfo_toplevel().navbar_title, self.winfo_toplevel().navbar_image, self.expand_navbar, self.centre_navbar)
            self.navbar.populate_navbar(self.winfo_toplevel().page_list)


class Page(Custom_Page, ctk.CTkFrame):
    pass

class Scrollable_Page(Custom_Page, ctk.CTkScrollableFrame):
    pass

class Navbar(ctk.CTkFrame):
    def __init__(self, master, title = None, image = None, expand = True, centered = True):
        super().__init__(master, border_width=1)
        self.title = title
        self.image = image
        self.master = master
        self.expand = expand
        self.centered = centered
        self.place_navbar()
    
    def place_navbar(self):
        master_columns = self.master.grid_size()[0]
        if self.expand:
            self.grid(row=0, column=0, columnspan=max(master_columns,1), sticky = "ew")
        else:
            if self.centered:
                self.grid(row=0, column=0, columnspan=max(master_columns,1))
            else:
                self.grid(row=0, column=0, columnspan=max(master_columns,1), sticky = "w")
            
    def populate_navbar(self, page_list):
        if self.title is not None:
            self.label = ctk.CTkButton(self,text=self.title, height=30, corner_radius=0, hover = False)
            self.label.grid(column=0, row=0, sticky="nsew")
            self.grid_columnconfigure(0, weight=1)

        if self.image is not None:
            self.Image = ctk.CTkButton(self,image=self.image, height=30, corner_radius=0, text="", width =30, hover = False)
            self.Image.grid(column=1, row=0, sticky="nsew")
            self.grid_columnconfigure(1, weight=1)

        self.buttons = []
        count = 0
        for page in page_list:
            if page.has_navbar is True or page.navbar_name is not None:
                #f frame needs to be used due to a binding issue taking the value of the wrong iteration of frame.
                p = page.identifier
                self.button = ctk.CTkButton(self, text=page.navbar_name, height=30, corner_radius=0, border_spacing=0, command=lambda p=p: self.winfo_toplevel().show_page(p))
                if page.navbar_name == self.master.navbar_name:
                    self.button.configure(fg_color = self.winfo_toplevel().theme_dampend_highlight_color) 
                self.buttons.append(self.button)
                self.buttons[count].grid(column=count+2, row=0, sticky="nsew")
                self.grid_columnconfigure(count+2, weight=1)
                count +=1
class CustomLabel(ctk.CTkLabel):
    """
    A Tkinter Label with wrapping capabilities.
    """
    def __init__(self, *args, wrappable: bool = False, wrap_padding: int = 100, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrap_padding = wrap_padding
        if wrappable:
            self.bind("<Configure>", self.update_wraplength)
    
    def update_wraplength(self, event = None):
        self.update_idletasks()
        self.configure(wraplength=self.master.winfo_width() - self.wrap_padding * ctk.ScalingTracker.get_widget_scaling(self))


class CCTKApplication(ctk.CTk, ctk.CTkFrame):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        