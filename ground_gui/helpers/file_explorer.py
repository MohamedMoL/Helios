from tkinter.filedialog import askopenfilename
from save_data import read_data


def browseFiles():
    filename = askopenfilename(initialdir="./",
                               title="Select a File",
                               filetypes=(("Text files",
                                           "*.txt*"),
                                          ("all files",
                                           "*.*")))
    if filename != "":
        read_data(filename)
