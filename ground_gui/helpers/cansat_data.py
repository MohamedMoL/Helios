from serial import Serial
from threading import Thread


class cansat:
    def __init__(self):
        # Cansat information

        self.infinite_loop = False

        self.keys = ["id_info", "pressure",
                     "temperature", "rotationX", "rotationY",
                     "rotationZ", "accelerationX", "accelerationY",
                     "accelerationZ", "latitude", "length", "uv_index", "altitude"]

        self.data = {key: "0" for key in self.keys}

        self.lists = {key: [] for key in self.keys}

        self.new_info = []

    def update_data_cansat(self, update_plots, insert_row):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:

            self.new_info = arduino.readline().decode("utf-8").strip().split(",")
            arduino.write(b'9')
            if len(self.new_info) == 13:  # If new info is received

                for data, value in zip(self.keys[:-1:], self.new_info[1::]):
                    self.data[data].set(value)
                    self.lists[data].append(float(value))

                altitude = round(self.calculate_altitude(
                    self.data["pressure"].get()), 2)

                self.data["altitude"].set(altitude)
                self.lists["altitude"].append(altitude)
                self.new_info.append(altitude)

                update_plots(
                    self.lists["id_info"], self.lists["temperature"], self.lists["pressure"])

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
        pressure = float(pressure) / 100
        altitude = 44330 * \
            (1.0 - pow(pressure / seaLevelhPa, 0.1903))
        return altitude


helios = cansat()
