# poseidon.py (Serial COM path) (mode)

# Poseidon --> [POSEIDON69 = COM#] <-- Ground Processing Application (Windows)
# Poseidon --> [/dev/serial#] <-- Ground Processing Application (POSIX?)

ENCRYPTION_KEY = None
ENCRYPTION_IV = None

CNC_INTERFACE = "\\\\.\\POSEIDON69"

class SensorData():
    # Pending Implementation
    pass

    def construct_binary_packet() -> bytes:
        # Pending Implementation
        pass

    def construct_text_packet() -> bytes:
        # Pending Implementation
        pass

def SendPacket(binary: bool, encrypted: bool, ecc : bool, ack: bool):
    # Pending Implementation
    if encrypted:
        pass
    else:
        pass

def CollectSensorData():
    # Pending Implementation
    sensor_data_collection = SensorData()
