from cube import pygame_cansat
from os import environ
from tkinter import Frame


class cansat3D(Frame):
    def __init__(self, controller):
        super().__init__(controller)

        self.WIDTH = 300
        self.HEIGHT = 300

        embed = Frame(self, width=self.WIDTH, height=self.HEIGHT) # creates embed frame for pygame window
        embed.pack(side = "left") # packs window to the left

        environ['SDL_WINDOWID'] = str(embed.winfo_id())

        self.pygame_rotate = pygame_cansat(self)

    def rotate_cube(self, pitch, roll, yaw):
        self.pygame_rotate.rotate_cube(pitch, roll, yaw)

