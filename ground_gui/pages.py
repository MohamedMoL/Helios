import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import random
matplotlib.use('TkAgg')


class window(tk.Tk):
    def __init__(self):
        super().__init__()

        container = tk.Frame(self)  # Will contain all pages
        self.wm_title("Hermes")  # Set window title

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

        self.variable_data = tk.IntVar(value=2)
        changeable = tk.Label(self, textvariable=self.variable_data)
        changeable.pack(pady=10, padx=10)

        label = tk.Label(self, text="Page One!!!")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Home))
        button1.pack()
        button3 = tk.Button(self, text="Change the data",
                            command=self.update_data)
        button3.pack()

    def update_data(self):
        self.variable_data.set(random.randint(0, 100))


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
