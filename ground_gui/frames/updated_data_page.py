from cansat_data import helios
from plots import Plots
from save_data import save_data, read_data
import tkinter as tk


class Data_page(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.plots = Plots()

        self.show_frame = controller.show_frame  # Refers to the tk.Tk()
        self.frames_methods = controller.frames

        # The frame that will contain all cansat labels and buttons
        self.labels_buttons_frame = tk.Frame(
            self, width=500, height=500)

        self.labels_buttons_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create all widgets
        self.create_labels()

        self.create_buttons()

        self.plots.set_plots(self)

    def create_labels(self):
        # ------------- Packet ID value + label ------------- #
        tk.Label(self.labels_buttons_frame, text="ID", height=3).grid(row=0, column=0)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Packet id"]).grid(
            row=0, column=1, padx=10, pady=10)
        
        # ------------- Time value + label ------------- #
        tk.Label(self.labels_buttons_frame, text="Time", height=3).grid(row=1, column=0)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Time"], width=15).grid(
            row=1, column=1, padx=10, pady=10)

        # ------------- Altitude value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="Altitude", height=3).grid(row=2, column=0)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Altitude"]).grid(
            row=2, column=1, padx=10, pady=10)

        # ------------- Pressure value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="Pressure", height=3).grid(row=3, column=0)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Pressure"]).grid(
            row=3, column=1, padx=10, pady=10)

        # ------------- Temperature value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="Temperature", height=3).grid(row=4, column=0)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Temperature"]).grid(
            row=4, column=1, padx=10, pady=10)

        # ------------- RotationX value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="RotationX").grid(row=0, column=2)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["RotationX"], width=15).grid(
            row=0, column=3, padx=10, pady=10)

        # ------------- RotationY value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="RotationY").grid(row=1, column=2)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["RotationY"]).grid(
            row=1, column=3, padx=10, pady=10)

        # ------------- RotationZ value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="RotationZ").grid(row=2, column=2)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["RotationZ"]).grid(
            row=2, column=3, padx=10, pady=10, sticky="EW")

        # ------------- AccelerationX value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="AccelerationX").grid(row=3, column=2)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationX"]).grid(
            row=3, column=3, padx=10, pady=10)

        # ------------- AccelerationY value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="AccelerationY").grid(row=4, column=2)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationY"]).grid(
            row=4, column=3, padx=10, pady=10)

        # ------------- AccelerationZ value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="AccelerationZ").grid(row=0, column=4)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["AccelerationZ"]).grid(
            row=0, column=5, padx=10, pady=10)

        # ------------- Latitude value + label ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="Latitude").grid(row=1, column=4)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Latitude"], width=10).grid(
            row=1, column=5, padx=10, pady=10, sticky="EW")

        # ------------- Length value ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="Length").grid(row=2, column=4)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["Length"]).grid(
            row=2, column=5, padx=10, pady=10, sticky="EW")

        # ------------- UV Index ------------- #
        tk.Label(self.labels_buttons_frame,
                 text="UV Index").grid(row=3, column=4)
        tk.Label(self.labels_buttons_frame, textvariable=helios.data["UV index"]).grid(
            row=3, column=5, padx=10, pady=10)
        
        # ------------- UV Color ------------- #
        tk.Label(self.labels_buttons_frame, bg="red").grid(row=4, column=4, columnspan=3, sticky="nsew")

    def create_buttons(self):
        back_home = tk.Button(self.labels_buttons_frame, text="Back to Home",
                              command=lambda: self.show_frame("Home"))
        back_home.grid(row=7, column=0, ipadx=10, ipady=10, pady=30)

        start_loop_button = tk.Button(self.labels_buttons_frame, text="Start",
                                      command=lambda: helios.start_loop(
                                          self.plots.update_plots,
                                          self.frames_methods["Show Info"].insert_row))
        start_loop_button.grid(row=7, column=1, ipadx=10, ipady=10)

        stop_loop_button = tk.Button(self.labels_buttons_frame, text="Stop",
                                     command=lambda: helios.stop_loop())
        stop_loop_button.grid(row=7, column=2, ipadx=10, ipady=10)

        save_data_button = tk.Button(self.labels_buttons_frame, text="Save",
                                     command=lambda: save_data(helios.lists))
        save_data_button.grid(row=7, column=3, ipadx=10, ipady=10)

        show_info_button = tk.Button(self.labels_buttons_frame, text="Show",
                                     command=lambda: self.show_frame("Show Info"))
        show_info_button.grid(row=7, column=4, ipadx=10, ipady=10)

        recover_info_button = tk.Button(self.labels_buttons_frame, text="Recover",
                                        command=lambda: read_data())
        recover_info_button.grid(row=7, column=5, ipadx=10, ipady=10)
