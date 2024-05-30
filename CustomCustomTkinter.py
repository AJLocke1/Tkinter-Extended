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

    def add_page(self, page):
        self.page_list.append(page)
        self.on_page_list_change()

    def on_page_list_change(self):
        for page in self.page_list:
            page.refresh_navbar()

    def show_page(self, identifier: str):
        for page in self.page_list:
            if page.identifier == identifier:
                page.lift()

class Custom_Page():
    """
    A better option for applications with multiple pages. Must use the grid manager.
    initialize the navbar in the application class after all pages are initialized.
    """
    def __init__(self, *args, identifier: str, has_navbar: bool, has_sidebar: bool, navbar_name: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = identifier
        self.has_navbar = has_navbar
        self.has_sidebar = has_sidebar
        self.navbar_name = navbar_name if navbar_name else identifier
        self.navbar = None

        self.column_offset = 1 if self.has_sidebar else 0
        self.row_offset = 1 if self.has_navbar else 0

        self.master.add_page(self)

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
                self.navbar = Navbar(self, self.master.navbar_title, self.master.navbar_image)
            self.navbar.populate_navbar(self.master.page_list)


class Page(Custom_Page, ctk.CTkFrame):
    pass

class Scrollable_Page(Custom_Page, ctk.CTkScrollableFrame):
    pass


class Navbar(ctk.CTkFrame):
    def __init__(self, master, title = None, image = None):
        super().__init__(master, border_width=1)
        self.title = title
        self.image = image
        self.master = master
        self.place_navbar()
    
    def place_navbar(self):
        master_columns = self.master.grid_size()[0]
        self.grid(row=0, column=0, columnspan=max(master_columns,1), sticky = "ew")
    
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
                self.buttons.append(ctk.CTkButton(self, text=page.navbar_name, height=30, corner_radius=0, command=lambda p=p: self.master.master.show_page(p)))
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
