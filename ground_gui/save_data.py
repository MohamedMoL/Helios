from datetime import datetime


def save_data(data):

    date_time_now = datetime.now()
    date = date_time_now.strftime("%d/%m/%Y %H:%M:%S")
    file_name = date_time_now.strftime("%d_%m_%Y_%H_%M_%S")

    with open(f"./recopilation_of_data/{file_name}.txt", "a") as my_file:
        my_file.write(f"# --- {date} --- #\n")
        for key in data:
            my_file.write(f"{key}:")
            my_file.write(",".join([str(num) for num in data[key]]))
            my_file.write("\n")


def read_data(file_root):
    with open(file_root, "r") as my_file:
        info = my_file.readlines()
        if info[0][0] == "#":
            for data in info[1::]:
                cansat_data = data.split(":")
                cansat_nums = cansat_data[1].strip().split(",")
                print(f"{cansat_data[0]}: {cansat_nums}")
