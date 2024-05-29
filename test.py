import CustomCustomTkinter as cctk
import customtkinter as ctk

class App(cctk.App):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("CustomTkinter Application")
        self.navbar_title = "App"
        self.geometry("400x300")

        self.initialize_pages()
        self.place_navbars()
    
    def initialize_pages(self):
        self.page_1 = Page_1(self, identifier="Page 1", has_navbar=True, has_sidebar=False)
        self.page_2 = Page_2(self, identifier="Page 2", has_navbar=True, has_sidebar=False)

    def update_label(self):
        self.label.configure(text="Button Clicked!")

class Page_1(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label1 = cctk.CustomLabel(self, text="Hello, CustomTkinter!", font=("Helvetica", 16), wrappable=True)
        self.add_widget(self.label1, row = 1, column = 0)

        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.show("Page 2"))
        self.add_widget(self.button, row = 2, column =0, pady=10)


class Page_2(cctk.Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = ctk.CTkButton(self, text="Change Page", command = lambda:self.show("Page 1"))
        self.add_widget(self.button, row = 0, column =0, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()