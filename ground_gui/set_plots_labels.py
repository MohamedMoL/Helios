def set_labels(plots, cansat_data_lists):
    plots[0].set_title('subplot 1')
    plots[0].set_ylabel('Temperature (º)')

    plots[1].set_title('subplot 2')
    plots[1].set_xlabel('Time (s)')
    plots[1].set_ylabel('Pressure (Pa)')

    plots[0].plot(cansat_data_lists["id_info"],
                  cansat_data_lists["temperature"])
    plots[1].plot(cansat_data_lists["id_info"],
                  cansat_data_lists["pressure"])

    plots[0].set_yticks(range(-20, 100, 20))
    plots[1].set_yticks(range(1_000_000, 10_000_001, 1_000_000))
