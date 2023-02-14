# import os
# import ctypes, sys

# def _is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False

# def _elevate():
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# if _is_admin():
#     print(os.path.realpath(os.path.dirname(__file__)))
#     print("hello world from an elevated process!")
#     input("Press enter to exit...")
# else:
#     _elevate()

from pynput.keyboard import Key, Listener
from time import sleep

def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

for i in range(100):
    print(i)
    sleep(1)