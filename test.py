import TkinterExtended as etk
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("App")    

        self.title_label = ctk.CTkLabel(self, text= "Test Application")
        self.title_label.grid(row = 0, column = 0)

        self.stack = etk.Stack(self, bg_color = "red")
        self.stack.grid(row = 1, column = 0)

        self.page1 = ctk.CTkFrame(self.stack, width=200, fg_color="blue")
        self.page2 = ctk.CTkFrame(self.stack, width=300, fg_color="green")
        self.page3 = ctk.CTkButton(self.stack, width = 150, fg_color="orange",text="page 1", command=lambda: self.stack.set_visible_child(self.page1))

        self.stack.add_widget(self.page1, "page1")
        self.stack.add_widget(self.page3, "page3")
        self.stack.add_widget(self.page2, "page2", 1)

        self.previous_button = ctk.CTkButton(self, text="previous", command=lambda: self.stack.show_previous())
        self.previous_button.grid(row=2, column=0)

        self.next_button = ctk.CTkButton(self, text="next", command=lambda: self.stack.show_next())
        self.next_button.grid(row=2, column=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()