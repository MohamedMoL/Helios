import tkinter as tk
from home import Home
from data_page import Data_page


class window(tk.Tk):
    def __init__(self, team_name):
        super().__init__()

        container = tk.Frame(self)  # Will contain all pages
        self.wm_title(team_name)  # Set window title

        # Create a fullscreen window
        self.attributes('-fullscreen', True)

        container.pack(side="top", fill="both", expand=True)

        # -------- Page changing --------- #
        self.frames = {"Home": "", "PageOne": ""}
        for key, frame in zip(self.frames.keys(), (Home, Data_page)):

            acual_frame = frame(container, self)

            self.frames[key] = acual_frame

            acual_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()  # Move the frame over other frames
