from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import figure, subplots_adjust


class Plots:
    def __init__(self):
        self.data_fig = self.create_figure()

        self.plots = self.create_plots(self.data_fig)

        self.configs = [{"ylabel": "Temperature (ºC)",
                               "title": "Evolution > Celsius/ms",
                               "color": "red"}, 
                               {"ylabel": "Pressure (Pa)",
                                "title": "Evolution > Pa/ms",
                                "color": "green"}]

    def create_figure(self):

        temp_press_time_fig = figure(figsize=(8, 8))
        temp_press_time_fig.set_facecolor("#F0F0F0")

        return temp_press_time_fig

    def create_plots(self, fig):
        plots = [fig.add_subplot(2, 1, 1), fig.add_subplot(
            2, 1, 2)]
        
        subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

        # Temperature plot
        plots[0].set_title('Evolution > Celsius/ms')
        plots[0].set_ylabel('Temperature (ºC)')
        plots[0].set_xlabel('Time (ms)')

        # Pressure plot
        plots[1].set_title('Evolution > Pa/ms')
        plots[1].set_xlabel('Time (ms)')
        plots[1].set_ylabel('Pressure (Pa)')

        return plots

    def set_plots(self, tk_frame):
        self.canvas = FigureCanvasTkAgg(self.data_fig, tk_frame)
        self.canvas.get_tk_widget().grid(row=0, rowspan=10, column=20)

    def update_plots(self, ids, info):
        for plot, conf, data in zip(self.plots, self.configs, info):
            plot.clear()
            self.update_each_plot(plot, ids, data, conf)

        # Re-draw the plots
        self.canvas.draw()

    def update_each_plot(self, plot, ids, data, conf):
        plot.set_title(conf["title"])
        plot.set_ylabel(conf["ylabel"])
        plot.set_xlabel('Time (ms)')
        plot.plot(ids, data, color=conf["color"])
