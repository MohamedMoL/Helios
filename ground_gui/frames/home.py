from tkinter import Frame, Label, Button


class Home(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Sets Helios' logo in the middle of the frame
        label = Label(self, image=controller.logo)
        label.place(relx=0.5, rely=0.5, anchor='center')

        Label(self, text="Home").pack(pady=10)

        # ------------ BUTTONS ------------ #
        Button(self, text="Data page", command=lambda: controller.show_frame("Data Page")).pack(pady=10)

        Button(self, text="Show info", command=lambda: controller.show_frame("Show Info")).pack(pady=10)

        Button(self, text="Quit", command=lambda: controller.quit()).pack(pady=10)
