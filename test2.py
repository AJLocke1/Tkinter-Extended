import TkinterExtended as etk
import customtkinter as ctk

class Page_stack(etk.Stack):
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.page1 = ctk.CTkFrame(self, bg_color="blue")
        self.page2 = ctk.CTkFrame(self, bg_color="green")

        self.add_widget(self.page1, "page1")
        self.add_widget(self.page2, "page2")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("App")    
        self.geometry("200x200") 

        self.title_label = ctk.CTkLabel(self, text= "Test Application")
        self.title_label.grid(row = 0, column = 0)

        self.stack = Page_stack(self, width = 200, height = 200, bg_color = "red")
        self.stack.grid(row = 1, column = 0)

        self.page1_button = ctk.CTkButton(self, text="page 1", command=lambda: self.stack.set_visible_child(self.stack.page1))
        self.page1_button.grid(row=2, column=0)

        self.page2_button = ctk.CTkButton(self, text="page 2", command=lambda: self.stack.set_visible_child("page2"))
        self.page2_button.grid(row=2, column=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()