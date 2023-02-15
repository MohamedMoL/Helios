# poseidon.py (Serial COM path) (mode)

# Poseidon --> [POSEIDON69 = COM#] <-- Ground Processing Application (Windows)
# Poseidon --> [/dev/serial#] <-- Ground Processing Application (POSIX?)

from poseidon_config import EmulatorConfiguration, get_config
from time import sleep
from random import randint, uniform, random
import serial

EMULATOR_CONFIG = get_config()

CNC_INTERFACE = "\\\\.\\POSEIDON69"

packet_count = 0

class NotImplementedException(Exception):
    pass

class SensorData():
    def __init__(self):
        global packet_count
        self.ID = "hermes"
        self.PacketID = packet_count
        packet_count += 1
        self.Altitude = round(uniform(0, 1000), 2)
        self.Pressure = round(uniform(1000000, 10000000), 2)
        self.Temperature = round(uniform(-20, 85), 2)
        self.RotationX = round(uniform(0, 360), 2)
        self.RotationY = round(uniform(0, 360), 2)
        self.RotationZ = round(uniform(0, 360), 2)
        self.AccelerationX = round(uniform(0, 4), 2)
        self.AccelerationY = round(uniform(0, 4), 2)
        self.AccelerationZ = round(uniform(0, 4), 2)
        self.Latitude = uniform(-90, 90)
        self.Longitude = uniform(-180, 180)
        self.UVIndex = round(uniform(0, 14), 2)

    def construct_binary_packet(self) -> bytes:
        raise NotImplementedException("Construct binary packet not implemented")

    def construct_text_packet(self) -> bytes:
        array = []
        for name in self.__dict__:
            array.append(self.__dict__[name])
        array = [str(x) for x in array]
        packet_str = ",".join(array)
        packet_str += "\r\n"
        packet_bytes = packet_str.encode("ASCII")
        return packet_bytes

def send_packet(sensor_data_collection: SensorData,
                serial_interface: serial.Serial,
                output_mode: str,
                ecc : bool,
                ack: bool,
                encrypted: bool,
                key: str = None):
    if output_mode == "text":
        data = sensor_data_collection.construct_text_packet()
    else:
        data = sensor_data_collection.construct_binary_packet()

    serial_interface.write(data)
    print(data.decode("ASCII"))

def initialize_emulator(cnc_interface : str = CNC_INTERFACE, com_interface : str = None, config : EmulatorConfiguration = EMULATOR_CONFIG):
    global CNC_INTERFACE
    print("Poseidon Engine started")
    print("Virtual COM Port:", cnc_interface)
    if com_interface is not None and type(com_interface) is str:
        print("Application should connect to:", com_interface)
    print("Configuration path:", config.config_path.absolute())

    CNC_INTERFACE = cnc_interface

    # Actual loop
    try:
        while True:
            if config.ecc_mode_enabled:
                raise NotImplementedException("(Error Correction Code not implemented)")
            if config.encryption_enabled:
                raise NotImplementedException("(Encryption not implemented)")
            if config.expect_ack:
                raise NotImplementedException("(Acknowledgement not implemented)")
            current_sensor_collection = SensorData()
            with serial.Serial("\\\\.\\" + CNC_INTERFACE, 9600, timeout=1) as cnc:
                send_packet(current_sensor_collection, cnc, config.output_mode, config.ecc_mode_enabled, config.expect_ack, config.encryption_enabled, config.encryption_keys)
                sleep(1)
    except KeyboardInterrupt:
        print("Detected CTRL+C, Shutting down Poseidon Engine")
        exit(0)
    except NotImplementedException as e:
        print(f"Function is not supported yet. {e}")
        print("Please check your configuration!")
        print("Poseidon is shutting down")
        exit(1)
    except Exception as e:
        print(f"An exception occurred: {e}")
        print("Poseidon is shutting down")
        exit(1)