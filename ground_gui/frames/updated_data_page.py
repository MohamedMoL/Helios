from cansat_data import helios
from plots import Plots
from save_data import save_data, read_data
from tkinter import Frame, Label, Button
from cansat3d import cansat3D


class Data_page(Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.plots = Plots()

        self.show_frame = controller.show_frame  # Refers to the tk.Tk()
        self.insert_row = controller.frames

        # The frame that will contain all cansat labels and buttons
        self.sat_frame = Frame(self, width=500, height=500)
        self.sat_frame.grid(row=0, column=0, padx=10)

        # The frame that will contain the 3D projection and the cansat's angles
        self.frame_3D = Frame(self, width=500, height=500)
        self.frame_3D.grid(row=1, column=0, padx=10, pady=10)

        # Create all widgets
        self.create_labels()

        self.create_buttons(self.sat_frame)

        self.plots.set_plots(self)

        self.cansat3D = cansat3D(self.frame_3D)
        self.cansat3D.grid(row=0, column=0, rowspan=4)

        # When a new packet arrives, update every widget
        helios.packet_id.trace("w", self.update_widgets)

    def update_widgets(self, v, i, m):

        self.plots.update_plots(helios.lists["Time"], helios.lists["Temperature"], helios.lists["Pressure"])

        self.insert_row["Show Info"].insert_row()
        
        self.cansat3D.rotate_cube(helios.data["AngleX"][1],
                    helios.data["AngleY"][1],
                    helios.data["AngleZ"][1])
        
        self.update_uv_color(int(helios.data["UV index"][1]))
        
    def update_uv_color(self, uv_index):
        for color, interval in helios.uv_color_intervals.items():
            if uv_index in interval:
                self.uv_color.config(bg=color)

    def create_label_structure(self, frame, lab_text, text_variable, lab_row, lab_col, lab_height=0, lab_width=0):
        Label(frame, text=lab_text, height=lab_height).grid(row=lab_row, column=lab_col)
        Label(frame, textvariable=text_variable, width=lab_width).grid(
            row=lab_row, column=lab_col + 1, padx=10, pady=10)
    
    def create_labels(self):
        # ------------- Packet ID value + label ------------- #
        self.create_label_structure(self.sat_frame, "ID", helios.packet_id, 0, 0, 3)
        
        # ------------- Time value + label ------------- #
        self.create_label_structure(self.sat_frame, "Time(ms)", helios.data["Time"][0], 1, 0, 3, 15)

        # ------------- Altitude value + label ------------- #
        self.create_label_structure(self.sat_frame, "Altitude(m)", helios.data["Altitude"][0], 2, 0, 3)

        # ------------- Pressure value + label ------------- #
        self.create_label_structure(self.sat_frame, "Pressure(Pa)", helios.data["Pressure"][0], 3, 0, 3)

        # ------------- Temperature value + label ------------- #
        self.create_label_structure(self.sat_frame, "Temperature(ºC)", helios.data["Temperature"][0], 4, 0, 3)

        # ------------- RotationX value + label ------------- #
        self.create_label_structure(self.sat_frame, "RotationX(deg/s^2)", helios.data["RotationX"][0], 0, 2, 3, 15)

        # ------------- RotationY value + label ------------- #
        self.create_label_structure(self.sat_frame, "RotationY(deg/s^2)", helios.data["RotationY"][0], 1, 2)

        # ------------- RotationZ value + label ------------- #
        self.create_label_structure(self.sat_frame, "RotationZ(deg/s^2)", helios.data["RotationZ"][0], 2, 2)

        # ------------- AccelerationX value + label ------------- #
        self.create_label_structure(self.sat_frame, "AccelerationX(m/s^2)", helios.data["AccelerationX"][0], 3, 2)

        # ------------- AccelerationY value + label ------------- #
        self.create_label_structure(self.sat_frame, "AccelerationY(m/s^2)", helios.data["AccelerationY"][0], 4, 2)

        # ------------- AccelerationZ value + label ------------- #
        self.create_label_structure(self.sat_frame, "AccelerationZ(m/s^2)", helios.data["AccelerationZ"][0], 0, 4)

        # ------------- Latitude value + label ------------- #
        self.create_label_structure(self.sat_frame, "Latitude", helios.data["Latitude"][0], 1, 4, lab_width=20)

        # ------------- Length value ------------- #
        self.create_label_structure(self.sat_frame, "Length", helios.data["Length"][0], 2, 4)

        # ------------- UV Index ------------- #
        self.create_label_structure(self.sat_frame, "UV Index", helios.data["UV index"][0], 3, 4)
        
        # ------------- UV Color ------------- #
        self.uv_color = Label(self.sat_frame)
        self.uv_color.grid(row=4, column=4, columnspan=3, sticky="nsew")

        # ------------- Pitch ------------- #
        self.create_label_structure(self.frame_3D, "Pitch(deg)", helios.data["AngleX"][0], 0, 1, lab_width=8)
        
        # ------------- Roll ------------- #
        self.create_label_structure(self.frame_3D, "Roll(deg)", helios.data["AngleY"][0], 1, 1)
        
        # ------------- Yaw ------------- #
        self.create_label_structure(self.frame_3D, "Yaw(deg)", helios.data["AngleZ"][0], 2, 1)

    def create_buttons(self, frame):
        configuration = {"row":7, "ipadx":10, "ipady":10, "pady":30}

        # ----------------- Back Home Button ----------------- #
        Button(frame, text="Back to Home", command=lambda: self.show_frame("Home")).grid(configuration, column=0)

        # ----------------- Start Loop Button ----------------- #
        Button(frame, text="Start", command=lambda: helios.start_loop()).grid(configuration, column=1)

        # ----------------- Stop Loop Button ----------------- #
        Button(frame, text="Stop", command=lambda: helios.stop_loop()).grid(configuration, column=2)

        # ----------------- Save Data Button ----------------- #
        Button(frame, text="Save", command=lambda: save_data(helios.lists)).grid(configuration, column=3)

        # ----------------- Show Info Button ----------------- #
        Button(frame, text="Show", command=lambda: self.show_frame("Show Info")).grid(configuration, column=4)

        # ----------------- Recover Info Button ----------------- #
        Button(frame, text="Recover", command=lambda: read_data()).grid(configuration, column=5)
