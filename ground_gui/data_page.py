from serial import Serial
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import threading
matplotlib.use('TkAgg')


class Data_page(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller  # Refers to the tk.Tk()

        # Will say if the "update_data_cansat" loop starts, continues or stops
        self.infinite_loop = True

        self.cansat_data_keys = ["id_info", "temperature", "altitude",
                                 "pressure", "accelerationX", "accelerationY",
                                 "accelerationZ", "rotationX", "rotationY",
                                 "rotationZ", "latitude", "length", "uv_index"]

        self.cansat_data = {key: tk.StringVar(
            value="0") for key in self.cansat_data_keys}

        # ----------------- Plot data ----------------- #
        self.time_datas = []
        self.temperature_datas = []
        self.pressure_datas = []

        self.create_labels()

        self.create_buttons()

        self.create_plots()

    def create_labels(self):
        # ------------- ID value + label ------------- #
        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, textvariable=self.cansat_data["id_info"], width=20).grid(
            row=0, column=1, padx=10, pady=10)

        # ------------- Temperature value + label ------------- #
        tk.Label(self, text="Temperature").grid(row=1, column=0)
        tk.Label(self, textvariable=self.cansat_data["temperature"]).grid(
            row=1, column=1, padx=10, pady=10)

        # ------------- Altitude value + label ------------- #
        tk.Label(self, text="Altitude").grid(row=2, column=0)
        tk.Label(self, textvariable=self.cansat_data["altitude"]).grid(
            row=2, column=1, padx=10, pady=10)

        # ------------- Pressure value + label ------------- #
        tk.Label(self, text="Pressure").grid(row=3, column=0)
        tk.Label(self, textvariable=self.cansat_data["pressure"]).grid(
            row=3, column=1, padx=10, pady=10)

        # ------------- AccelerationX value + label ------------- #
        tk.Label(self, text="AccelerationX").grid(row=4, column=0)
        tk.Label(self, textvariable=self.cansat_data["accelerationX"]).grid(
            row=4, column=1, padx=10, pady=10)

        # ------------- AccelerationY value + label ------------- #
        tk.Label(self, text="AccelerationY").grid(row=0, column=2)
        tk.Label(self, textvariable=self.cansat_data["accelerationY"]).grid(
            row=0, column=3, padx=10, pady=10)

        # ------------- AccelerationZ value + label ------------- #
        tk.Label(self, text="AccelerationZ").grid(row=1, column=2)
        tk.Label(self, textvariable=self.cansat_data["accelerationZ"]).grid(
            row=1, column=3, padx=10, pady=10)

        # ------------- RotationX value + label ------------- #
        tk.Label(self, text="RotationX").grid(row=2, column=2)
        tk.Label(self, textvariable=self.cansat_data["rotationX"]).grid(
            row=2, column=3, padx=10, pady=10)

        # ------------- RotationY value + label ------------- #
        tk.Label(self, text="RotationY").grid(row=3, column=2)
        tk.Label(self, textvariable=self.cansat_data["rotationY"]).grid(
            row=3, column=3, padx=10, pady=10)

        # ------------- RotationZ value + label ------------- #
        tk.Label(self, text="RotationZ").grid(row=4, column=2)
        tk.Label(self, textvariable=self.cansat_data["rotationZ"]).grid(
            row=4, column=3, padx=10, pady=10, sticky="E"+"W")

        # ------------- Latitude value + label ------------- #
        tk.Label(self, text="Latitude").grid(row=5, column=2)
        tk.Label(self, textvariable=self.cansat_data["latitude"], width=20).grid(
            row=5, column=3, padx=10, pady=10, sticky="E"+"W")

        # ------------- Length value ------------- #
        tk.Label(self, text="Length").grid(row=0, column=4)
        tk.Label(self, textvariable=self.cansat_data["length"]).grid(
            row=0, column=5, padx=10, pady=10, sticky="E"+"W")

        # ------------- UV Index ------------- #
        tk.Label(self, text="UV Index").grid(row=1, column=4)
        tk.Label(self, textvariable=self.cansat_data["uv_index"], width=20).grid(
            row=1, column=5, padx=10, pady=10)

    def create_buttons(self):
        back_home = tk.Button(self, text="Back to Home",
                              command=lambda: self.controller.show_frame("Home"))
        back_home.grid(row=7, column=0, ipadx=10, ipady=10)

        start_loop_button = tk.Button(self, text="Start",
                                      command=lambda: self.start_loop())
        start_loop_button.grid(row=7, column=1, ipadx=10, ipady=10)

        stop_loop_button = tk.Button(self, text="Stop",
                                     command=lambda: self.stop_loop())
        stop_loop_button.grid(row=7, column=2, ipadx=10, ipady=10)

    def update_data_cansat(self):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:
            start = time.perf_counter()
            # This will now timeout after 0.01s
            new_info = arduino.readline().decode("utf-8").strip().split(",")
            arduino.write(b'9')
            if len(new_info) == 14:  # If new info is received
                for data, value in zip(self.cansat_data_keys, new_info[1::]):
                    self.cansat_data[data].set(value)

                # ------- Plots data ------- #
                self.time_datas.append(int(new_info[1]))
                self.temperature_datas.append(float(new_info[4]))
                self.pressure_datas.append(float(new_info[3]))

                self.update_plots()

            end = time.perf_counter()
            # print("Esto tarda " + str(end - start))
            # If this is a loop, and the loop depends on external
            # self.after(1000, self.update_data_cansat)
            # flags to run, we can toggle the loop just by changing the self.infinite_loop flag, really good idea
            # By changing the if statement to a while statement, we no longer need self.after(), the loop and the
            # thread will take the job

        arduino.close()

    def stop_loop(self):
        self.infinite_loop = False
        # self._update_thread.join() # This will cause self.id.set(new_info[1]) to hang the process

    def start_loop(self):
        self.infinite_loop = True
        self._update_thread = threading.Thread(target=self.update_data_cansat)
        self._update_thread.start()

    def create_plots(self):

        temp_press_time_fig = plt.figure(figsize=(8, 8))

        # adding the subplot
        self.plots = [temp_press_time_fig.add_subplot(2, 1, 1), temp_press_time_fig.add_subplot(
            2, 1, 2)]

        self.canvas = FigureCanvasTkAgg(temp_press_time_fig, self)
        self.canvas.get_tk_widget().grid(pady=20, row=10, column=10)

    def update_plots(self):
        for current_plot in self.plots:
            current_plot.clear()

        self.plots[0].plot(self.time_datas, self.temperature_datas)
        self.plots[1].plot(self.time_datas, self.pressure_datas)

        self.canvas.draw()
