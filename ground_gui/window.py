import tkinter as tk
from threading import Thread
from home import Home
from updated_data_page import Data_page
from show_info_page import Show_info_page
from cansat_data import helios


class window(tk.Tk):
    def __init__(self, team_name):
        super().__init__()

        self.team_name = team_name

        container = tk.Frame(self)  # Will contain all pages
        self.wm_title(team_name)  # Set window title

        # Create a fullscreen window
        self.state("zoomed")

        container.pack(side="top", fill="both", expand=True)

        helios.data = {key: tk.StringVar(value="0") for key in helios.keys}

        # -------- Page changing --------- #
        self.frames = {"Home": "", "Data Page": "", "Show Info": ""}
        for key, frame in zip(self.frames.keys(), (Home, Data_page, Show_info_page)):

            acual_frame = frame(container, self)

            self.frames[key] = acual_frame

            acual_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()  # Move the frame over other frames
