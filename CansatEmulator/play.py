import poseidon

highest_galois_field_number = 255

for _ in range(100000):
    packet = poseidon.SensorData()
    ascii_text = packet.construct_text_payload()
    ascii_text_with_ecc = poseidon.RSCODEC.encode(ascii_text)
    ecc_code = ascii_text_with_ecc.lstrip(ascii_text)
    if ecc_code[-1] == 255 and ecc_code[-2] == 255:
        print(ecc_code)

print("Highest value in Galois field:", highest_galois_field_number)