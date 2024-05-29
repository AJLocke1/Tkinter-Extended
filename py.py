import tkinter as tk
import customtkinter as ctk  # Assuming ctk is imported correctly in your environment

class Page(tk.Frame):
    """
    A class for creating pages in a multi-page application.
    """
    def __init__(self, parent, *args, scrollable=False, identifier: str, has_navbar: bool, has_sidebar: bool, navbar_name: str = None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.identifier = identifier
        self.has_navbar = has_navbar
        self.has_sidebar = has_sidebar
        self.navbar_name = navbar_name
        
        if scrollable:
            # Use CTkScrollableFrame
            self._canvas = ctk.CTkScrollableFrame(self, *args, **kwargs)
            self._canvas.pack(fill=tk.BOTH, expand=tk.YES)
        else:
            # Use CTkFrame
            self._canvas = ctk.CTkFrame(self, *args, **kwargs)
            self._canvas.pack(fill=tk.BOTH, expand=tk.YES)
        
    def initialize_navbar(self, application):
        # Example of initializing a navbar
        if self.has_navbar:
            print(f"Initializing navbar for page '{self.identifier}' with name '{self.navbar_name}'")
            # Implement navbar initialization logic here

# Example of how to use the Page class
if __name__ == "__main__":
    
    class Application(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.pages = {}
            
            # Create pages
            #page1 = Page(self, scrollable=False, identifier="page1", has_navbar=True, has_sidebar=False)
            page2 = Page(self, scrollable=True, identifier="page2", has_navbar=True, has_sidebar=True, navbar_name="Sidebar")
            
            #self.pages["page1"] = page1
            self.pages["page2"] = page2
            
            # Initialize navbar after all pages are initialized
            self.initialize_navbars()
        
        def initialize_navbars(self):
            # Example of initializing navbars for all pages
            for page_id, page in self.pages.items():
                page.initialize_navbar(self)
        
    app = Application()
    app.mainloop()