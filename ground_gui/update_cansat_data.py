import time
import serial
info = {"team_name": "",
        "ID": 0,
        "altitude": 0,
        "pressure": 0,
        "temperature": 0,
        "rotationX": 0,
        "rotationY": 0,
        "rotationZ": 0,
        "accelerationX": 0,
        "accelerationY": 0,
        "accelerationZ": 0,
        "latitude": 0,
        "length": 0,
        "UV_index": 0}

def arduino_read_data():
    arduino = serial.Serial("COM5", 9600)
    time.sleep(2)
    new_info = arduino.readline().decode("utf-8").strip().split(",")
    for data, key in zip(new_info, list(info.keys())):
        info[key] = data
    arduino.write(b'9')
    arduino.close()

x = 0

while x <= 10:
    arduino_read_data()
    x += 1
