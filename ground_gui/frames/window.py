from PIL import Image, ImageTk
from cansat_data import helios
from show_info_page import Show_info_page
from updated_data_page import Data_page
from home import Home
from tkinter import Tk, Frame


class window(Tk):
    def __init__(self, team_name):
        super().__init__()

        self.team_name = team_name

        icon = Image.open("ground_gui/helios_logo.jpeg")
        # icon = icon.resize((900, 900), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(icon)

        container = Frame(self)  # Will contain all pages
        self.wm_title(team_name)  # Set window title
        self.iconphoto(False, self.logo) # Set icon image

        # Create a fullscreen window
        self.state("zoomed")

        container.pack()

        # Changes values to StringVar
        helios.transform_variable_to_tkinterVar()

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
