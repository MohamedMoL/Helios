import serial
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import random
import threading
matplotlib.use('TkAgg')


class window(tk.Tk):
    def __init__(self, team_name):
        super().__init__()

        container = tk.Frame(self)  # Will contain all pages
        self.wm_title(team_name)  # Set window title

        self.state('zoomed')  # Make the window use full screen

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # -------- Page changing --------- #
        self.frames = {}
        for F in (Home, PageOne, PageThree):

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

        label = tk.Label(self, text="Home")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Page one",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button3 = tk.Button(self, text="Page three",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()

        button4 = tk.Button(self, text="Quit",
                            command=lambda: controller.quit())
        button4.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.infinite_loop = True

        # ------------- ID value + label ------------- #
        self.id = tk.IntVar(value=0)
        tk.Label(self, text="ID").grid(row=0, column=0)
        tk.Label(self, textvariable=self.id).grid(
            row=0, column=1, padx=10, pady=10)

        # ------------- Temperature value + label ------------- #
        self.temperature = tk.DoubleVar(value=0)
        tk.Label(self, text="Temperature").grid(row=1, column=0)
        tk.Label(self, textvariable=self.temperature).grid(
            row=1, column=1, padx=10, pady=10)

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
            row=4, column=3, padx=10, pady=10)

        # ------------- Latitude value + label ------------- #
        self.latitude = tk.DoubleVar(value=0)
        tk.Label(self, text="Latitude").grid(row=5, column=2)
        tk.Label(self, textvariable=self.latitude).grid(
            row=5, column=3, padx=10, pady=10)

        # ------------- Length value + label ------------- #
        self.length = tk.DoubleVar(value=0)
        tk.Label(self, text="Length").grid(row=0, column=4)
        tk.Label(self, textvariable=self.length).grid(
            row=0, column=5, padx=10, pady=10)

        # ------------- UV Index value + label ------------- #
        self.uv_index = tk.DoubleVar(value=0)
        tk.Label(self, text="UV Index").grid(row=1, column=4)
        tk.Label(self, textvariable=self.uv_index).grid(
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

    def update_data_cansat(self):
        print("Started Receiver Thread")
        arduino = serial.Serial("COM5", 9600, timeout=0.01)
        while self.infinite_loop == True:
            start = time.perf_counter()
            new_info = arduino.readline().decode("utf-8").strip().split(",") # This will now timeout after 0.01s
            arduino.write(b'9')
            if len(new_info) == 14: # If new info is received
                self.id.set(new_info[1])
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
            end = time.perf_counter()
            #print("Esto tarda " + str(end - start))
            #self.after(1000, self.update_data_cansat) # If this is a loop, and the loop depends on external
            # flags to run, we can toggle the loop just by changing the self.infinite_loop flag, really good idea  
            # By changing the if statement to a while statement, we no longer need self.after(), the loop and the
            # thread will take the job
 
        arduino.close()
        print("Terminated Receiver Thread")
        return

    def stop_loop(self):
        self.infinite_loop = False
        #self._update_thread.join() # This will cause self.id.set(new_info[1]) to hang the process

    def start_loop(self):
        self.infinite_loop = True
        self._update_thread = threading.Thread(target=self.update_data_cansat)
        self._update_thread.start()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.pack()
        self.plot_data = [random.randint(0, 100) for _ in range(50)]

        self.createWidgets()

    def plot(self, canvas, plot1):
        plot1.clear()
        self.plot_data.append(random.randint(0, 100))
        plot1.plot(self.plot_data)
        canvas.draw()

    def createWidgets(self):

        fig = plt.figure(figsize=(8, 8))

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(self.plot_data)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.get_tk_widget().pack(pady=20)
        canvas.draw()

        plotbutton = tk.Button(
            text="plot", command=lambda: self.plot(canvas, plot1))
        plotbutton.pack()
