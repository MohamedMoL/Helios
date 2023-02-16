import time
import serial
info = {"team_name": "",
        "ID": 0,
        "altitude": 0,
        "pressure": 0,
        "rotationX": 0,
        "rotationY": 0,
        "rotationZ": 0,
        "accelerationX": 0,
        "accelerationY": 0,
        "accelerationZ": 0,
        "latitude": 0,
        "length": 0,
        "UV_index": 0}


def update_data(new_data):
    for data, key in zip(new_data, list(info.keys())):
        info[key] = data
    print(info)


arduino = serial.Serial("COM3", 9600)
time.sleep(2)
update_data(arduino.readline().decode("utf-8").split(","))
arduino.write(b'9')
arduino.close()
