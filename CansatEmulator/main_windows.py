from com0com_installer import get_virtual_pair_conf, install_com0com, uninstall_com0com
from poseidon_config import get_config, EmulatorConfiguration, configuration_wizard
from time import sleep, perf_counter
from pathlib import Path
import poseidon
import ctypes, sys

def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
        
def _elevate():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def check_first_run():
    return (get_virtual_pair_conf() is None) or (get_config() is None)

def first_run_procedure():
    print("Hi!👋")
    print("Looks like you're running this program for the first time.")
    if get_virtual_pair_conf() is None: 
        print("We need to install a virtual serial port driver in order for the emulator to work!")
        print("Checking Administrative privileges...")
        if _is_admin():
            print("This process is running in privileged mode. Continuing...")
            print("⚠️Warning: You're about to install a kernel driver: com0com. Press enter to install...")
            input()
            install_com0com()
        else:
            print("⚠️This process is currently running in user mode, administrative privilege is required")
            print("Press enter to request UAC Process elevation...")
            input()
            _elevate()
            exit(0)
    
    if get_config() is None:
        new_conf_path = Path("poseidon_conf")
        new_conf_path.touch()
        conf = EmulatorConfiguration(new_conf_path, True)
        conf.output_mode = "text"
        conf.ecc_mode_enabled = False
        conf.expect_ack = False
        conf.encryption_enabled = False
        conf.encryption_keys = None
    
    print("✔ Initialization sequence complete")
    print("Press enter to exit, and start this script again")
    input()
    exit(0)

def main():
    poseidon_config = get_config()
    cnc, com = get_virtual_pair_conf()
    configuration_wizard(poseidon_config)
    poseidon.initialize_emulator(cnc, com, poseidon_config)

if __name__ == "__main__":
    if check_first_run():
        first_run_procedure()
    else:
        main()