from datetime import datetime


def save_data(data):
    with open("cansat_data.txt", "a") as my_file:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        my_file.write(f"# --- {date} --- #\n")
        for key in data:
            my_file.write(f"{key}: ")
            my_file.write(",".join([str(num) for num in data[key]]))
            my_file.write("\n")
        my_file.write("\n")
