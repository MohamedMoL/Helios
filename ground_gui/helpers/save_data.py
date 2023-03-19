from datetime import datetime
from tkinter.filedialog import askopenfilename, askdirectory
from cansat_data import helios


def save_data(data):

    date_time_now = datetime.now()
    date = date_time_now.strftime("%d/%m/%Y %H:%M:%S")
    file_name = date_time_now.strftime("%d_%m_%Y_%H_%M_%S")

    file_path = askdirectory(initialdir="./", title="Select a folder")

    with open(f"{file_path}/{file_name}.txt", "w") as my_file:
        my_file.write(f"# --- {date} --- #")
        for key in data:
            my_file.write("\n")
            my_file.write(f"{key}:")
            my_file.write(";".join([str(num) for num in data[key]]))


def read_data():
    file_path = browseFiles()
    if file_path != "":
        with open(file_path, "r") as my_file:
            info = my_file.readlines()
            if info[0][0] == "#":
                for data in info[1::]:
                    cansat_data = data.split(":")
                    cansat_nums = cansat_data[1].strip().split(";")
                    cansat_nums = [float(num) for num in cansat_nums]
                    helios.lists[cansat_data[0]] = cansat_nums

def browseFiles():
    filename = askopenfilename(initialdir="./",
                               title="Select a file",
                               filetypes=(("Text files",
                                           "*.txt*"),
                                          ("all files",
                                           "*.*")))
    if filename != "":
        return filename