import os
import ctypes, sys

def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def _elevate():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if _is_admin():
    print(os.path.realpath(os.path.dirname(__file__)))
    print("hello world from an elevated process!")
    input("Press enter to exit...")
else:
    _elevate()