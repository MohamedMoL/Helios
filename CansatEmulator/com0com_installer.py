import os
from subprocess import PIPE, run
from zipfile import ZipFile
from locale import getpreferredencoding
from configparser import ConfigParser
import ctypes, sys
import shutil

ENCODING = getpreferredencoding()
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
COM0COM_PATH = os.path.join(SCRIPT_DIR, "com0com_akeo")
SETUPC_PATH = os.path.join(SCRIPT_DIR, "com0com_akeo", "setupc.exe")
COMPORT_INF_PATH = os.path.join(SCRIPT_DIR, "com0com_akeo", "comport.inf")

def _get_com_pair_list(stdin_decoded : str):
    # Strips the weird space at the beginning
    processed_str = stdin_decoded.strip()
    # Split in two and strips all of them
    processed_str = [x.strip() for x in processed_str.split("\n")]

    # CNCA0 PortName=POSEIDON69 --> Split =, extract the second part
    cnc_portname = processed_str[0].split("=")[1]

    # CNCB0 PortName=COM#,RealPortName=COM5 --> Split "," then get second part
    # RealPortName=COM5 --> Split = then get second part
    com_portname = processed_str[1].split(",")[1]\
                                    .split("=")[1]

    return (cnc_portname, com_portname)

# https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
def _is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_virtual_pair_conf():
    os.chdir(SCRIPT_DIR)

    try:
        config = ConfigParser()
        config.read("com0com_conf")
        cnc = config["Pair"]["CNC"]
        com = config["Pair"]["COM"]
    except:
        return None

    return (cnc, com)

def install_com0com():
    os.chdir(SCRIPT_DIR)

    if get_virtual_pair_conf() is not None:
        print("com0com has been already installed")
        return False

    if not _is_admin():
        print("Error, administrative privileges required!")
        return False

    # Unzips com0com_akeo.zip
    with ZipFile("com0com_akeo.zip") as com0com_archive:
        com0com_archive.extractall(SCRIPT_DIR)

    os.chdir(COM0COM_PATH)

    # Executes "setupc.exe --silent install PortName=POSEIDON69 PortName=COM#"
    process = run( [SETUPC_PATH, "--silent", "install", "PortName=POSEIDON69", "PortName=COM#,EmuBR=yes"], stdout=PIPE )
    print(">", " ".join([SETUPC_PATH, "--silent", "install", "PortName=POSEIDON69", "PortName=COM#,EmuBR=yes"]))
    print(process.stdout.decode(ENCODING))

    # Executes "pnputil.exe /add-driver comport.inf /install"
    process = run( ["pnputil.exe", "/add-driver", COMPORT_INF_PATH, "/install"], stdout=PIPE )
    print(">", " ".join(["pnputil.exe", "/add-driver", COMPORT_INF_PATH, "/install"]))
    print(process.stdout.decode(ENCODING))

    # Gets the port pair names
    process = run( [SETUPC_PATH, "--silent", "list"], stdout=PIPE )
    print(">", " ".join([SETUPC_PATH, "--silent", "list"]))
    print(process.stdout.decode(ENCODING))
    cnc, com = _get_com_pair_list(process.stdout.decode(ENCODING))

    # Write to configuration
    os.chdir(SCRIPT_DIR)
    with open("com0com_conf", "w") as configfile:
        config = ConfigParser()
        config['Pair'] = {"CNC": cnc, "COM": com}
        config['WARNING'] = { "line1": "Warning, DO NOT modify this configuration file as it contains crucial information for the program to run", \
            "line2": "No sections of this file can be modified. Modifying will cause the Poseidon engine to fail." }
        config.write(configfile)

    return True

def uninstall_com0com():
    if get_virtual_pair_conf() == None:
        print("com0com has not been installed")
        return False

    if not _is_admin():
        print("Error, administrative privileges required!")
        return False

    os.chdir(SCRIPT_DIR)
    
    # Remove configuration file
    os.remove("com0com_conf")

    os.chdir(COM0COM_PATH)

    # Run com0com uninstall command
    # Executes "setupc.exe --silent uninstall"
    process = run( [SETUPC_PATH, "--silent", "uninstall"], stdout=PIPE )
    print(">", " ".join([SETUPC_PATH, "--silent", "uninstall"]))
    print(process.stdout.decode(ENCODING))

    os.chdir(SCRIPT_DIR)
    shutil.rmtree('com0com_akeo', ignore_errors=True)

    return True