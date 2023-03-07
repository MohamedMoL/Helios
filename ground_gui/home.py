from tkinter import Frame, Label, Button


class Home(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Make the window use full screen
        self.config(width=screen_width, height=screen_height)
        self.pack_propagate(0)

        label = Label(self, text="Home")
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Data page",
                         command=lambda: controller.show_frame("Data Page"))
        button1.pack(pady=10, padx=10)

        button2 = Button(self, text="Show info",
                         command=lambda: controller.show_frame("Show Info"))
        button2.pack(pady=10, padx=10)

        button4 = Button(self, text="Quit",
                         command=lambda: controller.quit())
        button4.pack(pady=10, padx=10)
