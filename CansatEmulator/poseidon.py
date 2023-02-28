# Note that the implementation of everything in this file is kinda half assed
# Everything in here will be subject of breaking changes in the future.

# poseidon.py (Serial COM path) (mode)

# Poseidon --> [POSEIDON69 = COM#] <-- Ground Processing Application (Windows)
# Poseidon --> [/dev/serial#] <-- Ground Processing Application (POSIX?)

from poseidon_config import EmulatorConfiguration, get_config
from time import sleep
from random import randint, uniform, random, choice
from pathlib import Path
import serial
import reedsolo

ASCII_ART = \
    '''
  |      ,sss.  
| | |    $^,^$
|_|_|   _/$$$\_
  |   /'  ?$?  `.
  ;,-' /\ ,, /. |
  '-./' ;    ;: |
  |     |`  '|`,;
~~~~~~~~~~~~~~~~~~~~
'''

try:
    motd_path = (Path(__file__).parent / "motdlist")
    motdfile = open(str(motd_path), "r")
    motd_list = motdfile.read().split('\n')
    MOTD = choice(motd_list)
except:
    MOTD = ""
    pass

EMULATOR_CONFIG = get_config()

CNC_INTERFACE = "\\\\.\\POSEIDON69"

packet_count = 0

RSCODEC = reedsolo.RSCodec(48, 196)

class NotImplementedException(Exception):
    pass


class SensorData():
    def __init__(self):
        global packet_count
        self.ID = "Helios"
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

    def construct_binary_payload(self) -> bytes:
        raise NotImplementedException("Construct binary packet not implemented")

    def construct_text_payload(self) -> bytes:
        array = []
        for name in self.__dict__:
            array.append(self.__dict__[name])
        array = [str(x) for x in array]
        packet_str = ",".join(array)
        packet_bytes = packet_str.encode("ASCII")
        return packet_bytes
    
    def debug_print_payload(self):
        ascii_bytes = self.construct_text_payload()
        print(ascii_bytes.decode("ASCII"))


def send_packet(sensor_data_collection: SensorData,
                serial_interface: serial.Serial,
                output_mode: str,
                ecc: bool,
                ack: bool,
                encrypted: bool,
                key: str = None):
    
    # Generate sensor data payload
    if output_mode == "text":
        payload = sensor_data_collection.construct_text_payload()
    elif output_mode == 'binary':
        payload = sensor_data_collection.construct_binary_payload()

    # Encrypt the payload
    if encrypted:
        raise NotImplementedException("(Encryption not implemented)")

    # Generates error correction for the (encrypted/unencrypted) payload
    if ecc:
        payload = RSCODEC.encode(payload)
    
    # Surrounds the payload with Start of Packet and End of Packet
    # Or just append \r\n if it's in text mode

    if output_mode == 'text':
        payload += b'\r\n'
    else:
        raise NotImplementedException("(Error Correction Code not implemented)")

    serial_interface.write(payload)

    # Text mode debug output
    #print(payload.decode("ASCII"))
    sensor_data_collection.debug_print_payload()
    if ecc: print("+ECC")


def initialize_emulator(cnc_interface: str = CNC_INTERFACE, com_interface: str = None, config: EmulatorConfiguration = EMULATOR_CONFIG):
    global CNC_INTERFACE
    print(ASCII_ART)
    print("MOTD:", MOTD)
    print("Poseidon Engine started")
    print("Virtual COM Port:", cnc_interface)
    if com_interface is not None and type(com_interface) is str:
        print("Application should connect to:", com_interface)
    print("Configuration path:", config.config_path.absolute())

    CNC_INTERFACE = cnc_interface

    # Actual loop
    try:
        while True:
            if config.expect_ack:
                raise NotImplementedException(
                    "(Acknowledgement not implemented)")
            current_sensor_collection = SensorData()
            with serial.Serial("\\\\.\\" + CNC_INTERFACE, 9600, timeout=1) as cnc:
                send_packet(current_sensor_collection, cnc, config.output_mode, config.ecc_mode_enabled,
                            config.expect_ack, config.encryption_enabled, config.encryption_keys)
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
