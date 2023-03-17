from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure


class Plots:
    def __init__(self):
        self.data_fig = self.create_figure()

        self.plots = self.create_plots(self.data_fig)

    def create_figure(self):

        temp_press_time_fig = figure(figsize=(8, 8))
        temp_press_time_fig.suptitle("Plots")
        temp_press_time_fig.set_facecolor("#F0F0F0")

        return temp_press_time_fig

    def create_plots(self, fig):
        plots = [fig.add_subplot(2, 1, 1), fig.add_subplot(
            2, 1, 2)]

        # Temperature plot
        plots[0].set_title('subplot 1')
        plots[0].set_ylabel('Temperature (º)')

        # Pressure plot
        plots[1].set_title('subplot 2')
        plots[1].set_xlabel('Time (s)')
        plots[1].set_ylabel('Pressure (Pa)')

        return plots

    def set_plots(self, tk_frame):
        self.canvas = FigureCanvasTkAgg(self.data_fig, tk_frame)
        self.canvas.get_tk_widget().grid(pady=20, row=0, rowspan=10, column=2)

    def update_plots(self, ids, temperatures, pressures):
        for current_plot in self.plots:
            current_plot.clear()

        # Temperature plot
        self.plots[0].set_title('subplot 1')
        self.plots[0].set_ylabel('Temperature (º)')
        self.plots[0].plot(ids, temperatures)

        # Pressure plot
        self.plots[1].set_title('subplot 2')

        self.plots[1].set_xlabel('Time (s)')
        self.plots[1].set_ylabel('Pressure (Pa)')

        self.plots[1].plot(ids, pressures)

        # Re-draw the plots
        self.canvas.draw()
