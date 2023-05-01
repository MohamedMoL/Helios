from cube import pygame_cansat
from cansat_data import helios
from os import environ
from tkinter import Frame
from threading import Thread
from time import sleep


class cansat3D(Frame):
    def __init__(self, controller):
        super().__init__(controller)

        self.WIDTH = 300
        self.HEIGHT = 300

        self.config(width=self.WIDTH, height=self.HEIGHT)

        environ['SDL_WINDOWID'] = str(self.winfo_id())

        self.pygame_rotate = pygame_cansat(self)

        self.continue_rotating = False

    def rotate_cube(self):
        while self.continue_rotating:
            sleep(0.1)
            self.pygame_rotate.degrees_to_radians(helios.data["AngleX"][1],
                        helios.data["AngleY"][1],
                        helios.data["AngleZ"][1])
            
    def start_rotating_loop(self):
        self.continue_rotating = True
        if self.continue_rotating:
            Thread(target=self.rotate_cube).start()

    def stop_rotating_loop(self):
        self.continue_rotating = False
