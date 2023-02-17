import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import random
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

        # ------------- Cansat data instances ------------- #
        self.id = tk.IntVar(value=0)
        self.temperature = tk.DoubleVar(value=0)
        self.altitude = tk.DoubleVar(value=0)
        self.pressure = tk.DoubleVar(value=0)
        self.accelerationX = tk.DoubleVar(value=0)
        self.accelerationY = tk.DoubleVar(value=0)
        self.accelerationZ = tk.DoubleVar(value=0)
        self.rotationX = tk.DoubleVar(value=0)
        self.rotationY = tk.DoubleVar(value=0)
        self.rotationZ = tk.DoubleVar(value=0)
        self.latitude = tk.DoubleVar(value=0)
        self.length = tk.DoubleVar(value=0)
        self.uv_index = tk.DoubleVar(value=0)

        id_label = tk.Label(self, text="ID")
        id_label.grid(row=1, column=0)
        id_data = tk.Label(self, textvariable=self.id)
        id_data.grid(row=1, column=1)

        temperature_label = tk.Label(self, text="Temperature")
        temperature_label.grid(row=2, column=0)
        temperature_data = tk.Label(self, textvariable=self.temperature)
        temperature_data.grid(row=2, column=1)

        altitude_label = tk.Label(self, text="Altitude")
        altitude_label.grid(row=3, column=0)
        altitude_data = tk.Label(self, textvariable=self.altitude)
        altitude_data.grid(row=3, column=1)

        pressure_label = tk.Label(self, text="Pressure")
        pressure_label.grid(row=4, column=0)
        pressure_data = tk.Label(self, textvariable=self.pressure)
        pressure_data.grid(row=4, column=1)

        accelerationX_label = tk.Label(self, text="Acceleration X")
        accelerationX_label.grid(row=5, column=0)
        accelerationX_data = tk.Label(self, textvariable=self.accelerationX)
        accelerationX_data.grid(row=5, column=1) 

        label = tk.Label(self, text="Page One!!!")
        label.grid(row=6, column=0)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.grid(row=7, column=0)


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
        canvas.get_tk_widget().pack()
        canvas.draw()

        plotbutton = tk.Button(
            text="plot", command=lambda: self.plot(canvas, plot1))
        plotbutton.pack()
