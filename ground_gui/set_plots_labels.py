def set_labels(plots, cansat_data_lists):

    # Temperature plot
    plots[0].set_title('subplot 1')
    plots[0].set_ylabel('Temperature (º)')
    plots[0].plot(cansat_data_lists["id_info"],
                  cansat_data_lists["temperature"])

    # Pressure plot
    plots[1].set_title('subplot 2')

    plots[1].set_xlabel('Time (s)')
    plots[1].set_ylabel('Pressure (Pa)')

    plots[1].plot(cansat_data_lists["id_info"],
                  cansat_data_lists["pressure"])
