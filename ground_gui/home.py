import tkinter as tk


class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Make the window use full screen
        self.config(width=screen_width, height=screen_height)
        self.pack_propagate(0)

        label = tk.Label(self, text="Home")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Page one",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack(pady=10, padx=10)

        button4 = tk.Button(self, text="Quit",
                            command=lambda: controller.quit())
        button4.pack(pady=10, padx=10)
