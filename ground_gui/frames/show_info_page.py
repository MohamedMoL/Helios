from cansat_data import helios
from tkinter.ttk import Style, Treeview, Scrollbar
import tkinter as tk

class Show_info_page(tk.Frame):
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
        container = tk.Frame(
            self, width=self.winfo_screenwidth(), height=treeview_height)

        container.pack()
        container.pack_propagate(0)

        # Treeview instance
        self.treeview = Treeview(
            container, columns=helios.keys)

        # Scrollbar instance + config
        vscrollbar = Scrollbar(self.treeview, orient=tk.VERTICAL)
        vscrollbar.config(command=self.treeview.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview config
        self.treeview.config(yscrollcommand=vscrollbar.set)

        # Treeview columns / headings
        self.treeview.heading("#0", text="Packet ID")
        self.treeview.column(column="#0", anchor="center",
                             width=column_width, stretch=0)

        for i in helios.keys:
            self.treeview.heading(i, text=i)
            self.treeview.column(column=i, anchor="center",
                                 width=column_width, stretch=0)

        self.treeview.pack(expand=True, fill="both")

        container.pack()
        container.pack_propagate(0)

        # Buttons instances
        back_home_button = tk.Button(self, text="Back to Home",
                                     command=lambda: controller.show_frame("Home"))
        back_home_button.pack(padx=20, pady=20, side="top")

        data_page_button = tk.Button(self, text="Data page",
                                     command=lambda: controller.show_frame("Data Page"))
        data_page_button.pack(padx=20, side="top")

    def insert_row(self):
        self.treeview.insert(
            "", 
            tk.END, 
            text=helios.packet_id.get(),
            values=[value.get() for value in helios.data.values()])
        
        self.treeview.yview_moveto(1)
