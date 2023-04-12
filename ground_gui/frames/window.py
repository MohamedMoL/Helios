from PIL import Image, ImageTk
from cansat_data import helios
from show_info_page import Show_info_page
from updated_data_page import Data_page
from home import Home
from tkinter import Tk, Frame


class window(Tk):
    def __init__(self, team_name, logo_path):
        super().__init__()

        self.team_name = team_name

        icon = Image.open(logo_path)
        # icon = icon.resize((900, 900), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(icon)

        container = Frame(self).grid()  # Will contain all pages
        self.wm_title(team_name)  # Set window title
        self.iconphoto(False, self.logo) # Set icon image

        # Create a fullscreen window
        self.state("zoomed")

        # Changes values to StringVar
        helios.transform_variables_to_tkinterVar()

        # -------- Page changing --------- #
        self.frames = {"Home": Home, "Data Page": Data_page, "Show Info": Show_info_page}
        for key, frame in self.frames.items():

            self.frames[key] = frame(container, self)
            self.frames[key].grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, cont):

        self.frames[cont].tkraise()  # Move the frame over other frames
