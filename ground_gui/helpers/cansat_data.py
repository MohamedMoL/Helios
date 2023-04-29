from serial import Serial
from threading import Thread
from tkinter import DoubleVar


class cansat:
    def __init__(self):
        
        self.infinite_loop = False

        self.updateable = True

        self.uv_color_intervals = {
            "green": [0, 1, 2],
            "yellow": [3, 4, 5],
            "orange": [6, 7],
            "red": [8, 9, 10],
            "purple": [11, 12, 13, 14, 15, 16]
        }

        """ 
        --------------- The order of the data fields is important --------------
        ID,Time,Pressure,Temperature,Altitude,VelocityRotationX,VelocityRotationY,
        VelocityRotationZ,AccelerationX,AccelerationY,AccelerationZ,AngleX,
        AngleY,AngleZ,Latitude,Longitude,UVIndex
        ------------------------------------------------------------------------
        """
        self.keys = ["Time", "Pressure", "Temperature", "Altitude",
                    "RotationX", "RotationY", "RotationZ",
                    "AccelerationX", "AccelerationY", "AccelerationZ",
                    "AngleX", "AngleY", "AngleZ", "Latitude",
                    "Length", "UV index"]

        self.lists = {key: [] for key in self.keys}

    def update_data_cansat(self):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:

            new_info = arduino.readline().decode("utf-8").strip().split(",")
            
            if len(new_info) == 17:  # If new info is received

                new_info_nums = [float(num) for num in new_info[1::]]

                for key, value in zip(self.keys, new_info_nums):
                    self.data[key][0].set(value)
                    self.data[key][1] = value
                    self.lists[key].append(value)

                self.packet_id.set(self.packet_id.get() + 1)

        arduino.close()
    
    def transform_variables_to_tkinterVar(self):
        self.data = {key: [DoubleVar(value=0), 0] for key in self.keys}
        self.packet_id = DoubleVar(value=0)

    def start_loop(self):
        if not self.infinite_loop and self.updateable:
            self.infinite_loop = True
            _update_thread = Thread(target=self.update_data_cansat)
            _update_thread.start()

    def stop_loop(self):
        self.infinite_loop = False

    def update_all_data_fields(self, field, data_list):
        self.lists[field] = data_list

        self.data[field][0].set(data_list[-1])
        self.data[field][1] = data_list[-1]

        if field == self.keys[-1]: 
            self.updateable = False
            self.infinite_loop = False
            self.packet_id.set(len(data_list))
            

helios = cansat()
