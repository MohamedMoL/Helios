#%%
# [HELIOS]  [Payload]   [ECC]
#  ASCII     60Bytes   48 Bytes
import os
import serial
import struct
import reedsolo

HAS_ECC = True
HEADER_NAME = "Helios"
#COM_PORT = "COM4"
COM_PORT = "\\\\.\\POSEIDON69"
com = serial.Serial(COM_PORT, 9600, timeout=2)
RSCODEC = reedsolo.RSCodec(48, 108)

class SensorData():
    def __init__(self):
        self.Time = 0xffffffff # 32 bit/4 bytes unsigned long
        self.Pressure = float('nan')
        self.Temperature = float('nan')
        self.Altitude = float('nan')
        self.VelocityRotationX = float('nan')
        self.VelocityRotationY = float('nan')
        self.VelocityRotationZ = float('nan')
        self.AccelerationX = float('nan')
        self.AccelerationY = float('nan')
        self.AccelerationZ = float('nan')
        self.AngleX = float('nan')
        self.AngleY = float('nan')
        self.AngleZ = float('nan')
        self.Latitude = float('nan')
        self.Longitude = float('nan')
        self.UVIndex = float('nan')
        self.foundErrors = None
        self.errataAmount = None
        self.payload = None
        self.ecc = None

def DisplayPacket(d : SensorData):
    os.system("cls") # Windows oriented code, I'm a disgrace to humanity
    data = f"""Time:\t\t\t{d.Time}
Pressure:\t\t{d.Pressure}
Temperature:\t\t{d.Temperature}
Altitude:\t\t{d.Altitude}
VelocityRotationX:\t{d.VelocityRotationX}
VelocityRotationY:\t{d.VelocityRotationY}
VelocityRotationZ:\t{d.VelocityRotationZ}
AccelerationX:\t\t{d.AccelerationX}
AccelerationY:\t\t{d.AccelerationY}
AccelerationZ:\t\t{d.AccelerationZ}
AngleX:\t\t\t{d.AngleX}
AngleY:\t\t\t{d.AngleY}
AngleZ:\t\t\t{d.AngleZ}
Latitude:\t\t{d.Latitude}
Longitude:\t\t{d.Longitude}
UVIndex:\t\t{d.UVIndex}"""
    print(data)
    print("Payload:", d.payload.hex())
    if d.ecc != None:
        print("ECC:", d.ecc.hex())
    if d.foundErrors:
        if d.Time == 0xffffffff or d.errataAmount == None:
            print("Unable to recover data from error")
        else:
            print(f"Found {d.errataAmount} error(s)")
    
def receive_packet() -> SensorData:
    new_sd = SensorData()
    com.read_until(b'Helios') # This will read in: (garbage)Helios
    # If no garbase data is found, the length of this will be always 6
    # Helio ASCII word is used for synchronization and a marker for the packet
    payload = com.read(64)
    if HAS_ECC:
        ecc = com.read(48)
        new_sd.ecc = ecc
    new_sd.payload = payload
    try:
        if HAS_ECC:
            packet = payload + ecc
            payload, ecc_symbols, errata_pos = RSCODEC.decode(packet)
            new_sd.foundErrors = (errata_pos != b'')
            new_sd.errataAmount = len(list(errata_pos))
        format_code = "Lfffffffffffffff"
        unpacked_struct = struct.unpack(format_code, payload)
        for name, val in zip(new_sd.__dict__.keys(), unpacked_struct):
            new_sd.__dict__[name] = val
    except Exception as e:
        new_sd.foundErrors = True
        print(e)
    return new_sd
#%%
def main():
    for _ in range(1000):
        received_sensor_data = receive_packet()
        os.system("cls")
        DisplayPacket(received_sensor_data)

if __name__ == "__main__":
    main()