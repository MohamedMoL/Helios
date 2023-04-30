from datetime import datetime
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import askyesno
from cansat_data import helios


def save_data():

    date_time_now = datetime.now()
    date = date_time_now.strftime("%d/%m/%Y %H:%M:%S")
    file_name = date_time_now.strftime("%d_%m_%Y_%H_%M_%S")

    file_path = askdirectory(initialdir="./", title="Select a folder")

    with open(f"{file_path}/{file_name}.csv", "w") as my_file:
        my_file.write(f"# --- {date} --- #\n")
        my_file.write(";".join(helios.keys))
        all_data_nums = [[value[id] for value in helios.lists.values()] for id in range(0, len(helios.lists["Time"]))]
        for packet in all_data_nums:
            my_file.write("\n")
            my_file.write(";".join([str(num) for num in packet]))

    with open(f"{file_path}/{file_name}.txt", "w") as my_file:
        my_file.write(f"# --- {date} --- #")
        for key in helios.lists:
            my_file.write("\n")
            my_file.write(f"{key}:")
            my_file.write(";".join([str(num) for num in helios.lists[key]]))

def read_data():
    permission_for_recover = askyesno(message="You won't be able to read more data from Cansat. Are you sure?", 
             title="Recover data warning")
    if permission_for_recover:
        file_path = browseFiles()
        if file_path != "":
            with open(file_path, "r") as my_file:
                info = my_file.readlines()
                if info[0][0] == "#":
                    for data in info[1::]:
                        cansat_data = data.split(":")
                        cansat_nums = [float(num) for num in cansat_data[1].strip().split(";")]
                        helios.update_all_data_fields(cansat_data[0], cansat_nums)

def browseFiles():
    filename = askopenfilename(initialdir="./",
                               title="Select a file",
                               filetypes=(("Text files",
                                           "*.txt*"),
                                          ("all files",
                                           "*.*")))
    if filename != "":
        return filename