from cansat_data import helios
from plots import Plots
from save_data import save_data, read_data
from tkinter import Frame, Label, Button
from cansat3d import cansat3D


class Data_page(Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.plots = Plots()

        self.show_frame = controller.show_frame  # Refers to the tk.Tk()
        self.frames_methods = controller.frames

        # The frame that will contain all cansat labels and buttons
        self.labels_buttons_frame = Frame(
            self, width=500, height=500)

        self.labels_buttons_frame.grid(row=0, column=0, padx=10)

        # The frame that will contain the 3D projection and the cansat's angles
        self.cansat3D_frame = Frame(
            self, width=500, height=500)

        self.cansat3D_frame.grid(row=1, column=0, padx=10, pady=10)

        # Create all widgets
        self.create_labels()

        self.create_buttons()

        self.plots.set_plots(self)

        self.cansat3D = cansat3D(self.cansat3D_frame)

        self.cansat3D.grid(row=0, column=0, rowspan=4)
        self.create_angles_labels()

    def create_labels(self):
        # ------------- Packet ID value + label ------------- #
        Label(self.labels_buttons_frame, text="ID", height=3).grid(row=0, column=0)
        Label(self.labels_buttons_frame, textvariable=helios.packet_id).grid(
            row=0, column=1, padx=10, pady=10)
        
        # ------------- Time value + label ------------- #
        Label(self.labels_buttons_frame, text="Time(ms)", height=3).grid(row=1, column=0)
        Label(self.labels_buttons_frame, textvariable=helios.data["Time"], width=15).grid(
            row=1, column=1, padx=10, pady=10)

        # ------------- Altitude value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="Altitude(m)", height=3).grid(row=2, column=0)
        Label(self.labels_buttons_frame, textvariable=helios.data["Altitude"]).grid(
            row=2, column=1, padx=10, pady=10)

        # ------------- Pressure value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="Pressure(Pa)", height=3).grid(row=3, column=0)
        Label(self.labels_buttons_frame, textvariable=helios.data["Pressure"]).grid(
            row=3, column=1, padx=10, pady=10)

        # ------------- Temperature value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="Temperature(ºC)", height=3).grid(row=4, column=0)
        Label(self.labels_buttons_frame, textvariable=helios.data["Temperature"]).grid(
            row=4, column=1, padx=10, pady=10)

        # ------------- RotationX value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="RotationX(deg/s^2)").grid(row=0, column=2)
        Label(self.labels_buttons_frame, textvariable=helios.data["RotationX"], width=15).grid(
            row=0, column=3, padx=10, pady=10)

        # ------------- RotationY value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="RotationY(deg/s^2)").grid(row=1, column=2)
        Label(self.labels_buttons_frame, textvariable=helios.data["RotationY"]).grid(
            row=1, column=3, padx=10, pady=10)

        # ------------- RotationZ value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="RotationZ(deg/s^2)").grid(row=2, column=2)
        Label(self.labels_buttons_frame, textvariable=helios.data["RotationZ"]).grid(
            row=2, column=3, padx=10, pady=10, sticky="EW")

        # ------------- AccelerationX value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="AccelerationX(m/s^2)").grid(row=3, column=2)
        Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationX"]).grid(
            row=3, column=3, padx=10, pady=10)

        # ------------- AccelerationY value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="AccelerationY(m/s^2)").grid(row=4, column=2)
        Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationY"]).grid(
            row=4, column=3, padx=10, pady=10)

        # ------------- AccelerationZ value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="AccelerationZ(m/s^2)").grid(row=0, column=4)
        Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationZ"]).grid(
            row=0, column=5, padx=10, pady=10)

        # ------------- Latitude value + label ------------- #
        Label(self.labels_buttons_frame,
                 text="Latitude").grid(row=1, column=4)
        Label(self.labels_buttons_frame, textvariable=helios.data["Latitude"], width=20).grid(
            row=1, column=5, padx=10, pady=10, sticky="EW")

        # ------------- Length value ------------- #
        Label(self.labels_buttons_frame,
                 text="Length").grid(row=2, column=4)
        Label(self.labels_buttons_frame, textvariable=helios.data["Length"]).grid(
            row=2, column=5, padx=10, pady=10, sticky="EW")

        # ------------- UV Index ------------- #
        Label(self.labels_buttons_frame,
                 text="UV Index").grid(row=3, column=4)
        Label(self.labels_buttons_frame, textvariable=helios.data["UV index"]).grid(
            row=3, column=5, padx=10, pady=10)
        
        # ------------- UV Color ------------- #
        Label(self.labels_buttons_frame, bg="red").grid(row=4, column=4, columnspan=3, sticky="nsew")

    def create_angles_labels(self):
        # ------------- Pitch ------------- #
        Label(self.cansat3D_frame,
                 text="Pitch").grid(row=0, column=1)
        Label(self.cansat3D_frame, textvariable=helios.data["AngleX"], width=8).grid(
            row=0, column=2, padx=10, pady=10)
        
        # ------------- Roll ------------- #
        Label(self.cansat3D_frame,
                 text="Roll").grid(row=1, column=1)
        Label(self.cansat3D_frame, textvariable=helios.data["AngleY"]).grid(
            row=1, column=2, padx=10, pady=10)
        
        # ------------- Yaw ------------- #
        Label(self.cansat3D_frame,
                 text="Yaw").grid(row=2, column=1)
        Label(self.cansat3D_frame, textvariable=helios.data["AngleZ"]).grid(
            row=2, column=2, padx=10, pady=10)

    def create_buttons(self):
        back_home = Button(self.labels_buttons_frame, text="Back to Home",
                              command=lambda: self.show_frame("Home"))
        back_home.grid(row=7, column=0, ipadx=10, ipady=10, pady=30)

        start_loop_button = Button(self.labels_buttons_frame, text="Start",
                                      command=lambda: helios.start_loop(
                                          self.plots.update_plots,
                                          self.frames_methods["Show Info"].insert_row, 
                                          self.cansat3D.rotate_cube))
        start_loop_button.grid(row=7, column=1, ipadx=10, ipady=10)

        stop_loop_button = Button(self.labels_buttons_frame, text="Stop",
                                     command=lambda: helios.stop_loop())
        stop_loop_button.grid(row=7, column=2, ipadx=10, ipady=10)

        save_data_button = Button(self.labels_buttons_frame, text="Save",
                                     command=lambda: save_data(helios.lists))
        save_data_button.grid(row=7, column=3, ipadx=10, ipady=10)

        show_info_button = Button(self.labels_buttons_frame, text="Show",
                                     command=lambda: self.show_frame("Show Info"))
        show_info_button.grid(row=7, column=4, ipadx=10, ipady=10)

        recover_info_button = Button(self.labels_buttons_frame, text="Recover",
                                        command=lambda: read_data())
        recover_info_button.grid(row=7, column=5, ipadx=10, ipady=10)
