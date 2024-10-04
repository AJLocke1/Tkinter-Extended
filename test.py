import CustomCustomTkinter as cctk
import customtkinter as ctk

class App(cctk.App):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("CustomTkinter Application")
        self.geometry("400x300")

        self.page_1 = Page_1(self, identifier="Page 1", has_navbar=True, has_sidebar=False, expand_navbar = True, centre_navbar = True)
        self.page_2 = Page_2(self, identifier="Page 2", has_navbar=True, has_sidebar=False, expand_navbar = True, centre_navbar = True)
        self.page_3 = Page_3(self, identifier="Page 3", has_navbar=True, has_sidebar=False, expand_navbar = True, centre_navbar = True)
        self.page_4 = Page_4(self, identifier="Page 4", has_navbar=True, has_sidebar=False, expand_navbar = True, centre_navbar = True)

        self.show_page("Page 1")

    def update_label(self):
        self.label.configure(text="Button Clicked!")

class Page_1(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = cctk.CustomLabel(self, wrappable=True, text = "Page 1")
        self.add_widget(self.label, row = 0, column =0, pady=10)
        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.winfo_toplevel().show_page("Page 1"))
        self.add_widget(self.button, row = 2, column =0, pady=10)


class Page_2(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = cctk.CustomLabel(self, wrappable=True, text = "Page 2")
        self.add_widget(self.label, row = 0, column =0, pady=10)
        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.winfo_toplevel().show_page("Page 1"))
        self.add_widget(self.button, row = 2, column =0, pady=10)

class Page_3(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = cctk.CustomLabel(self, wrappable=True, text = "Page 3")
        self.add_widget(self.label, row = 0, column =0, pady=10)
        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.winfo_toplevel().show_page("Page 1"))
        self.add_widget(self.button, row = 2, column =0, pady=10)

class Page_4(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = cctk.CustomLabel(self, wrappable=True, text = "Page 4")
        self.add_widget(self.label, row = 0, column =0, pady=10)
        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.winfo_toplevel().show_page("Page 1"))
        self.add_widget(self.button, row = 2, column =0, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()