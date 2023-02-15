info = {"ID": 0,
        "altitude": 0,
        "pressure": 0,
        "rotation": [0, 0, 0],  # X, Y, Z
        "acceleration": [0, 0, 0],  # X, Y, Z
        "latitude": 0,
        "length": 0,
        "UV_index": 0}


def update_data(new_data):
    info["ID"] += 1
    for data, key in zip(new_data, list(info.keys())[1:]):
        info[key] = data
    print(info)


update_data([100, 200, [2, 4, 0], [20, 10, 8], 2000, 6000, 2])
