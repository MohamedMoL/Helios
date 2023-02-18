import serial
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
import matplotlib
import threading
matplotlib.use('TkAgg')
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1) # https://stackoverflow.com/questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
# WINDOWS ONLY

class window(tk.Tk):
    def __init__(self, team_name):
        super().__init__()
        self.call('tk', 'scaling', 1.25)

        container = tk.Frame(self)  # Will contain all pages
        self.wm_title(team_name)  # Set window title

        # Create a fullscreen window
        self.attributes('-fullscreen', True)

        container.pack(side="top", fill="both", expand=True)

        # -------- Page changing --------- #
        self.frames = {}
        for F in (Home, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()  # Move the frame over other frames


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
                            command=lambda: controller.show_frame(PageOne))
        button1.pack(pady=10, padx=10)

        button4 = tk.Button(self, text="Quit",
                            command=lambda: controller.quit())
        button4.pack(pady=10, padx=10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.infinite_loop = True

        # ------------- ID value + label ------------- #
        self.id = tk.IntVar(value=0)
        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, textvariable=self.id, width=20).grid(
            row=0, column=1, padx=10, pady=10)

        self.time_datas = []

        # ------------- Temperature value + label ------------- #
        self.temperature = tk.DoubleVar(value=0)
        tk.Label(self, text="Temperature").grid(row=1, column=0)
        tk.Label(self, textvariable=self.temperature).grid(
            row=1, column=1, padx=10, pady=10)

        self.temperature_datas = []

        # ------------- Altitude value + label ------------- #
        self.altitude = tk.DoubleVar(value=0)
        tk.Label(self, text="Altitude").grid(row=2, column=0)
        tk.Label(self, textvariable=self.altitude).grid(
            row=2, column=1, padx=10, pady=10)

        # ------------- Pressure value + label ------------- #
        self.pressure = tk.DoubleVar(value=0)
        tk.Label(self, text="Pressure").grid(row=3, column=0)
        tk.Label(self, textvariable=self.pressure).grid(
            row=3, column=1, padx=10, pady=10)

        self.pressure_datas = []

        # ------------- AccelerationX value + label ------------- #
        self.accelerationX = tk.DoubleVar(value=0)
        tk.Label(self, text="AccelerationX").grid(row=4, column=0)
        tk.Label(self, textvariable=self.accelerationX).grid(
            row=4, column=1, padx=10, pady=10)

        # ------------- AccelerationY value + label ------------- #
        self.accelerationY = tk.DoubleVar(value=0)
        tk.Label(self, text="AccelerationY").grid(row=0, column=2)
        tk.Label(self, textvariable=self.accelerationY).grid(
            row=0, column=3, padx=10, pady=10)

        # ------------- AccelerationZ value + label ------------- #
        self.accelerationZ = tk.DoubleVar(value=0)
        tk.Label(self, text="AccelerationZ").grid(row=1, column=2)
        tk.Label(self, textvariable=self.accelerationZ).grid(
            row=1, column=3, padx=10, pady=10)

        # ------------- RotationX value + label ------------- #
        self.rotationX = tk.DoubleVar(value=0)
        tk.Label(self, text="RotationX").grid(row=2, column=2)
        tk.Label(self, textvariable=self.rotationX).grid(
            row=2, column=3, padx=10, pady=10)

        # ------------- RotationY value + label ------------- #
        self.rotationY = tk.DoubleVar(value=0)
        tk.Label(self, text="RotationY").grid(row=3, column=2)
        tk.Label(self, textvariable=self.rotationY).grid(
            row=3, column=3, padx=10, pady=10)

        # ------------- RotationZ value + label ------------- #
        self.rotationZ = tk.DoubleVar(value=0)
        tk.Label(self, text="RotationZ").grid(row=4, column=2)
        tk.Label(self, textvariable=self.rotationZ).grid(
            row=4, column=3, padx=10, pady=10, sticky="E"+"W")

        # ------------- Latitude value + label ------------- #
        self.latitude = tk.DoubleVar(value=0)
        tk.Label(self, text="Latitude").grid(row=5, column=2)
        tk.Label(self, textvariable=self.latitude, width=20).grid(
            row=5, column=3, padx=10, pady=10, sticky="E"+"W")

        # ------------- Length value + label ------------- #
        self.length = tk.DoubleVar(value=0)
        tk.Label(self, text="Length").grid(row=0, column=4)
        tk.Label(self, textvariable=self.length).grid(
            row=0, column=5, padx=10, pady=10, sticky="E"+"W")

        # ------------- UV Index value + label ------------- #
        self.uv_index = tk.DoubleVar(value=0)
        tk.Label(self, text="UV Index").grid(row=1, column=4)
        tk.Label(self, textvariable=self.uv_index, width=20).grid(
            row=1, column=5, padx=10, pady=10)

        label = tk.Label(self, text="Page One!!!")
        label.grid(row=7, column=7)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.grid(row=7, column=0)

        start_loop_button = tk.Button(self, text="Start",
                                      command=lambda: self.start_loop())
        start_loop_button.grid(row=7, column=1)

        stop_button = tk.Button(self, text="Stop",
                                command=lambda: self.stop_loop())
        stop_button.grid(row=7, column=2)

        tk.Button(self, text="plot").grid(row=10, column=10)

        self.createWidgets()

    def update_data_cansat(self):
        # print("Started Receiver Thread")
        arduino = serial.Serial("COM5", 9600, timeout=0.01)
        while self.infinite_loop == True:
            start = time.perf_counter()
            # This will now timeout after 0.01s
            new_info = arduino.readline().decode("utf-8").strip().split(",")
            arduino.write(b'9')
            if len(new_info) == 14:  # If new info is received
                self.id.set(int(new_info[1]))
                self.altitude.set(new_info[2])
                self.pressure.set(new_info[3])
                self.temperature.set(new_info[4])
                self.rotationX.set(new_info[5])
                self.rotationY.set(new_info[6])
                self.rotationZ.set(new_info[7])
                self.accelerationX.set(new_info[8])
                self.accelerationY.set(new_info[9])
                self.accelerationZ.set(new_info[10])
                self.latitude.set(new_info[11])
                self.length.set(new_info[12])
                self.uv_index.set(new_info[13])

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
        # print("Terminated Receiver Thread")

    def stop_loop(self):
        self.infinite_loop = False
        # self._update_thread.join() # This will cause self.id.set(new_info[1]) to hang the process

    def start_loop(self):
        self.infinite_loop = True
        self._update_thread = threading.Thread(target=self.update_data_cansat)
        self._update_thread.start()

    def createWidgets(self):

        #temp_press_time_fig = Figure(figsize=(8, 8))
        temp_press_time_fig = plt.figure(figsize=(8, 8))

        # adding the subplot
        self.temp_time_plot = temp_press_time_fig.add_subplot(2, 1, 1)
        self.press_time_plot = temp_press_time_fig.add_subplot(
            2, 1, 2, sharex=self.temp_time_plot)

        self.canvas1 = FigureCanvasTkAgg(temp_press_time_fig, self)
        self.canvas1.get_tk_widget().grid(pady=20, row=10, column=10)
        self.canvas1.draw()

    def update_plots(self):
        self.temp_time_plot.clear()
        self.press_time_plot.clear()

        self.temp_time_plot.plot(self.time_datas, self.temperature_datas)
        self.press_time_plot.plot(self.time_datas, self.pressure_datas)

        self.canvas1.draw()
