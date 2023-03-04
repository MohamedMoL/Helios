from serial import Serial


class cansat:
    def __init__(self):
        # Cansat information

        self.infinite_loop = False

        self.keys = ["id_info", "altitude", "pressure",
                     "temperature", "rotationX", "rotationY",
                     "rotationZ", "accelerationX", "accelerationY",
                     "accelerationZ", "latitude", "length", "uv_index"]

        self.data = {key: "0" for key in self.keys}

        self.lists = {key: [] for key in self.keys}

        self.new_info = []

    def update_data_cansat(self, update_plots, insert_row):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:

            self.new_info = arduino.readline().decode("utf-8").strip().split(",")
            arduino.write(b'9')
            if len(self.new_info) == 14:  # If new info is received

                for data, value in zip(self.keys, self.new_info[1::]):
                    self.data[data].set(value)
                    self.lists[data].append(float(value))

                update_plots()
                insert_row()

        arduino.close()


helios = cansat()
