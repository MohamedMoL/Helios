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

    def create_label_structure(self, frame, lab_text, text_variable, lab_row, lab_col, lab_height=0, lab_width=0):
        Label(frame, text=lab_text, height=lab_height).grid(row=lab_row, column=lab_col)
        Label(frame, textvariable=text_variable, width=lab_width).grid(
            row=lab_row, column=lab_col + 1, padx=10, pady=10)
    
    def create_labels(self):
        # ------------- Packet ID value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "ID", helios.packet_id, 0, 0, lab_height=3)
        
        # ------------- Time value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Time(ms)", helios.data["Time"], 1, 0, lab_height=3, lab_width=15)

        # ------------- Altitude value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Altitude(m)", helios.data["Altitude"], 2, 0, lab_height=3)

        # ------------- Pressure value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Pressure(Pa)", helios.data["Pressure"], 3, 0, lab_height=3)

        # ------------- Temperature value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Temperature(ºC)", helios.data["Temperature"], 4, 0, lab_height=3)

        # ------------- RotationX value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "RotationX(deg/s^2)", helios.data["RotationX"], 0, 2, lab_height=3, lab_width=15)

        # ------------- RotationY value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "RotationY(deg/s^2)", helios.data["RotationY"], 1, 2)

        # ------------- RotationZ value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "RotationZ(deg/s^2)", helios.data["RotationZ"], 2, 2)

        # ------------- AccelerationX value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "AccelerationX(m/s^2)", helios.data["AccelerationX"], 3, 2)

        # ------------- AccelerationY value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "AccelerationY(m/s^2)", helios.data["AccelerationY"], 4, 2)

        # ------------- AccelerationZ value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "AccelerationZ(m/s^2)", helios.data["AccelerationZ"], 0, 4)

        # ------------- Latitude value + label ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Latitude", helios.data["Latitude"], 1, 4, lab_width=20)

        # ------------- Length value ------------- #
        self.create_label_structure(self.labels_buttons_frame, "Length", helios.data["Length"], 2, 4)

        # ------------- UV Index ------------- #
        self.create_label_structure(self.labels_buttons_frame, "UV Index", helios.data["UV index"], 3, 4)
        
        # ------------- UV Color ------------- #
        Label(self.labels_buttons_frame, bg="red").grid(row=4, column=4, columnspan=3, sticky="nsew")

        # ------------- Pitch ------------- #
        self.create_label_structure(self.cansat3D_frame, "Pitch", helios.data["AngleX"], 0, 1, lab_width=8)
        
        # ------------- Roll ------------- #
        self.create_label_structure(self.cansat3D_frame, "Roll", helios.data["AngleY"], 1, 1)
        
        # ------------- Yaw ------------- #
        self.create_label_structure(self.cansat3D_frame, "Yaw", helios.data["AngleZ"], 2, 1)

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
