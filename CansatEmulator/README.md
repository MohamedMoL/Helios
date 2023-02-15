# CanSat Emulator (Poseidon)

This is an emulator of the real CanSat. It uses virtual serial port to emulate the radio transmission device (UART) with randomly generated values being sent back.

This is developed in order to speed up the ground application's development process.

**This emulator is written for Windows, there is no support for Linux or MacOS yet.**

## Installation

You need:
- A Windows Computer
- Administrative account

1. Open a terminal with administrator rights
2. Navigate to this folder (CansatEmulator)
3. Install dependencies `pip install -r requirements.txt`
4. Run `python main_windows.py`, the program will instruct you
5. You may start using the emulator now by executing the same command as step 4, and press `Enter`.

Note: if you see "unrecognized command", you should check your PATH variable.

Subsequent executions of command `python main_windows.py` would not require an privileged terminal anymore.

## Uninstall

To uninstall, open up a command prompt with administrative privileges, navigate to CansatEmulator and execute the following command:
`python main_windows.py uninstall`

This will remove the Poseidon configuration file and the com0com virtual serial port driver as well.

## Usage
Via commandline:
`python main_windows.py`

This will bring up an configuration menu. You can configure how the emulator behaves by enabling or disabling some of its protocol features.
```
Poseidon Engine - Configuration / Launcher

Output Format: text - [V]
Error correction: False - [B]
Expect Ack Packets: False - [N]
Enable Encryption: False - [M]
Encryption Key: None - Please edit poseidon_conf file

Press [Enter] to start the Poseidon Engine
Press [V], [B], [N], [M] to change the respective settings
```

Pressing `Enter` will start the emulator. Note that if no application is attached to the emulator's COM port, the application will not respond. Even pressing `CTRL+C`.

After attaching an process to the COM port, the emulator will print out what is exactly being sent.

```
Poseidon Engine - Configuration / Launcher

Output Format: text - [V]
Error correction: False - [B]
Expect Ack Packets: False - [N]
Enable Encryption: False - [M]
Encryption Key: None - Please edit poseidon_conf file

Press [Enter] to start the Poseidon Engine
Press [V], [B], [N], [M] to change the respective settings
Poseidon Engine started
Virtual COM Port: POSEIDON69
Application should connect to: COM5
Configuration path: C:\Users\qt\Repository\maspa_cansat\CansatEmulator\poseidon_conf
hermes,0,202.83,6784963.15,-17.75,277.51,20.02,357.88,0.53,2.52,1.52,-69.61135591546874,20.472343225916802,5.02

hermes,1,922.28,6006688.63,82.88,294.75,105.51,200.61,2.79,3.21,0.49,61.41025081377836,138.7792539031496,13.88

hermes,2,645.12,6662869.1,10.48,58.71,219.08,343.4,0.14,0.5,1.52,43.2130352399532,-128.46716784626386,10.82

hermes,3,110.8,2172500.72,26.71,267.35,77.78,104.24,1.63,3.83,0.09,79.24059939767179,150.50543911919107,2.05

hermes,4,12.44,3214305.62,58.33,248.9,251.23,60.05,0.27,3.67,3.96,6.732475129203763,172.82388341176005,6.4

hermes,5,590.71,7960365.23,-18.72,334.22,154.31,54.25,3.53,0.7,0.6,-19.362909985883988,-37.34590845674643,1.41

hermes,6,730.59,7817228.54,-17.41,14.75,343.5,326.02,3.07,3.64,2.1,-72.07425712125452,3.834111120759559,5.23

hermes,7,937.61,6081594.84,58.91,343.15,20.09,193.77,0.26,0.73,2.62,-23.910271485077843,-10.242802208595293,7.24
```

You can stop the emulator by pressing `CTRL+C`.