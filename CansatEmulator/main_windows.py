from com0com_installer import get_virtual_pair_conf, install_com0com, uninstall_com0com
from config import get_config

import ctypes, sys

def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
        
def _elevate():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def check_first_run():
    return (get_virtual_pair_conf() is None) and (get_config() is None)

def main():
    print("Windows - Poseidon (CanSat Emulator) Launcher")


if __name__ == "__main__":
    main()