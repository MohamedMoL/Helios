from cansat_data import helios
from tkinter.ttk import Style, Treeview, Scrollbar
from tkinter import Frame, Button

class Show_info_page(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Set treeview style
        treeview_style = Style()
        treeview_style.theme_use('clam')
        treeview_style.configure('Treeview', rowheight=40)

        # Treeview dimensions
        treeview_height = int(self.winfo_screenheight() / 10 * 8.5)
        column_width = int(self.winfo_screenwidth() / 17)

        # Create the frame that will contain the treeview
        container = Frame(
            self, width=self.winfo_screenwidth(), height=treeview_height)
        container.pack()
        container.pack_propagate(0)

        # Treeview instance
        self.treeview = Treeview(
            container, columns=helios.keys)
        self.treeview.pack(expand=True, fill="both")

        # Scrollbar instance + config
        vscrollbar = Scrollbar(self.treeview, orient="vertical")
        vscrollbar.config(command=self.treeview.yview)
        vscrollbar.pack(side="right", fill="y")

        # Treeview config
        self.treeview.config(yscrollcommand=vscrollbar.set)

        # Treeview columns / headings
        self.treeview.heading("#0", text="Packet ID")
        self.treeview.column(column="#0", anchor="center",
                             width=column_width, stretch=0)

        for header in helios.keys:
            self.treeview.heading(header, text=header)
            self.treeview.column(column=header, anchor="center",
                                 width=column_width, stretch=0)

        # Buttons instances
        Button(self, text="Back to Home", command=lambda: controller.show_frame("Home")).pack(pady=20, side="top")

        Button(self, text="Data page", command=lambda: controller.show_frame("Data Page")).pack(side="top")

    def insert_row(self):
        self.treeview.insert(
            "", 
            "end", 
            text=helios.packet_id.get(),
            values=[value[1] for value in helios.data.values()])
        
        self.treeview.yview_moveto(1)

    def insert_all_rows(self):
        all_data_nums = [[value[id] for value in helios.lists.values()] for id in range(0, len(helios.lists["Time"]))]

        for packet_id, cansat_values in enumerate(all_data_nums, start=1):
            self.treeview.insert(
            "", 
            "end", 
            text=packet_id,
            values=cansat_values)
        
        self.treeview.yview_moveto(1)
