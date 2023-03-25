from tkinter import Frame, Label, Button


class Home(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Make the window use full screen
        self.config(width=screen_width, height=screen_height)
        self.pack_propagate(0)

        label = Label(self, image=controller.logo)
        label.image = controller.logo
        label.place(relx=0.5, rely=0.5, anchor='center')

        label = Label(self, text="Home")
        label.pack(pady=10, padx=10)

        go_to_data_page = Button(self, text="Data page",
                         command=lambda: controller.show_frame("Data Page"))
        go_to_data_page.pack(pady=10, padx=10)

        go_to_info_table_page = Button(self, text="Show info",
                         command=lambda: controller.show_frame("Show Info"))
        go_to_info_table_page.pack(pady=10, padx=10)

        close_window = Button(self, text="Quit",
                         command=lambda: controller.quit())
        close_window.pack(pady=10, padx=10)
