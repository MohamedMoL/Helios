import tkinter as tk
from tkinter.ttk import Style, Treeview, Scrollbar
from cansat_data import helios


class Show_info_page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        treeview_style = Style()
        treeview_style.theme_use('clam')

        # Add the rowheight
        treeview_style.configure('Treeview', rowheight=40)

        screen_width = int(self.winfo_screenwidth() / 13)

        self.controller = controller

        # Treeview instance
        self.treeview = Treeview(
            self, columns=helios.keys[1::])

        # Scrollbars instances

        vscrollbar = Scrollbar(self.treeview, orient=tk.VERTICAL)

        # Treeview config
        self.treeview.config(yscrollcommand=vscrollbar.set)

        self.treeview.heading("#0", text="Time")
        self.treeview.column(column="#0", width=screen_width, stretch=0)

        for i in helios.keys[1::]:
            self.treeview.heading(i, text=i)
            self.treeview.column(column=i, width=screen_width, stretch=0)

        self.treeview.pack(expand=True, fill="both")

        # Scrollbars config
        vscrollbar.config(command=self.treeview.yview)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons instances
        back_home_button = tk.Button(self, text="Back to Home",
                                     command=lambda: self.controller.show_frame("Home"))
        back_home_button.pack(padx=20, pady=20)

        data_page_button = tk.Button(self, text="Data page",
                                     command=lambda: controller.show_frame("Data Page"))
        data_page_button.pack(pady=20, padx=20)

    def insert_row(self):
        self.treeview.insert("", tk.END, text=str(
            helios.new_info[1]), values=helios.new_info[2::])
        self.treeview.yview_moveto(1)
