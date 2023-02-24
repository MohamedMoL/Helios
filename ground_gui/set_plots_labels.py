def set_labels(self):
    self.plots[0].set_title('subplot 1')
    self.plots[0].set_ylabel('Temperature (º)')

    self.plots[1].set_title('subplot 2')
    self.plots[1].set_xlabel('Time (s)')
    self.plots[1].set_ylabel('Pressure (Pa)')

    self.plots[0].plot(self.cansat_data_lists["id_info"],
                       self.cansat_data_lists["temperature"])
    self.plots[1].plot(self.cansat_data_lists["id_info"],
                       self.cansat_data_lists["pressure"])
