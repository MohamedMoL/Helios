from serial import Serial
from threading import Thread


class cansat:
    def __init__(self):
        # Cansat information

        self.infinite_loop = False

        self.keys = ["Time", "Pressure", "Temperature",
                    "RotationX", "RotationY", "RotationZ",
                    "AccelerationX", "AccelerationY", "AccelerationZ",
                    "Latitude", "Length", "UV index", "Altitude"]

        self.data = {key: "0" for key in self.keys}
        self.data["Packet id"] = "0"

        self.lists = {key: [] for key in self.keys}

    def update_data_cansat(self, update_plots, insert_row):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:

            new_info = arduino.readline().decode("utf-8").strip().split(",")
            new_info_nums = [float(num) for num in new_info[1::]]
            arduino.write(b'9')
            if len(new_info) == 13:  # If new info is received

                for data, value in zip(self.keys[:-1:], new_info_nums):
                    self.data[data].set(value)
                    self.lists[data].append(value)

                self.data["Packet id"].set(self.data["Packet id"].get() + 1)

                altitude = round(self.calculate_altitude(
                    self.data["Pressure"].get()), 2)

                self.data["Altitude"].set(altitude)
                self.lists["Altitude"].append(altitude)

                update_plots(
                    self.lists["Time"], self.lists["Temperature"], self.lists["Pressure"])

                insert_row()

        arduino.close()

    def start_loop(self, update_plots, insert_row):
        if not helios.infinite_loop:
            helios.infinite_loop = True
            self._update_thread = Thread(
                target=helios.update_data_cansat, args=(update_plots, insert_row))
            self._update_thread.start()

    def stop_loop(self):
        helios.infinite_loop = False

    def calculate_altitude(self, pressure, seaLevelhPa=1019):
        pressure /= 100
        altitude = 44330 * \
            (1.0 - pow(pressure / seaLevelhPa, 0.1903))
        return altitude


helios = cansat()
