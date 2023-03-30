from serial import Serial
from threading import Thread
from tkinter import DoubleVar


class cansat:
    def __init__(self):
        
        self.infinite_loop = False

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
                    

        self.data = 0 # {key: "0" for key in self.keys}
        self.packet_id = 0

        self.lists = {key: [] for key in self.keys}

    def update_data_cansat(self, update_plots, insert_row, rotate_cube):
        arduino = Serial("COM3", 9600, timeout=0.01)
        while self.infinite_loop == True:

            new_info = arduino.readline().decode("utf-8").strip().split(",")
            new_info_nums = [float(num) for num in new_info[1::]]
            if len(new_info_nums) == 16:  # If new info is received

                for key, value in zip(self.keys, new_info_nums):
                    self.data[key].set(value)
                    self.lists[key].append(value)

                self.packet_id.set(self.packet_id.get() + 1)

                update_plots(
                    self.lists["Time"], self.lists["Temperature"], self.lists["Pressure"])

                insert_row()

                rotate_cube(
                    self.data["AngleX"].get(),
                    self.data["AngleY"].get(),
                    self.data["AngleZ"].get())

        arduino.close()
    
    def transform_variable_to_tkinterVar(self):
        self.data = {key: DoubleVar(value=0) for key in self.keys}
        self.packet_id = DoubleVar(value=0)

    def start_loop(self, update_plots, insert_row, rotate_cube):
        if not self.infinite_loop:
            self.infinite_loop = True
            _update_thread = Thread(
                target=self.update_data_cansat, args=(update_plots, insert_row, rotate_cube))
            _update_thread.start()

    def stop_loop(self):
        self.infinite_loop = False


helios = cansat()
