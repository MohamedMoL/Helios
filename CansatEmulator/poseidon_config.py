# 4 Sections:
# Text mode / Binary mode
# Error Correction / No Error Correction
# Enable Acknowledgement packet / Disable Acknowledgement packet
# Enable Encryption / Disable Encryption
# (Encryption key: KEY:IV)

from pathlib import Path
from configparser import ConfigParser
from helper import clear
from pynput.keyboard import Key, Listener

def get_config():
    if Path("poseidon_conf").exists():
        return EmulatorConfiguration(Path("poseidon_conf"))
    else:
        return None

def _yesno_to_bool(x : str):
    if x.lower() == "yes":
        return True
    elif x.lower() == "no":
        return False
    elif x == None:
        return None
    else:
        raise ValueError("The input must be an string of 'yes' or 'no'")
    
def _bool_to_yesno(x : bool):
    if x == True:
        return "yes"
    elif x == False:
        return "no"
    elif x == None:
        return None
    else:
        raise ValueError("The input must be a boolean")

class EmulatorConfiguration():
    _output_mode = None
    _ecc_mode_enabled = None
    _expect_ack = None
    _encryption_enabled = None
    _encryption_keys = None

    def __init__(self, config_path : Path, empty: bool = False):
        self.config_path = config_path
        if not empty:
            # If the file is not empty, read the configuration
            config = ConfigParser(allow_no_value=True)
            config.read( str(config_path) )
            
            self._output_mode = config['Poseidon']['OutputMode']
            self._ecc_mode_enabled = _yesno_to_bool(config['Poseidon']['EnableErrorCorrection'])
            self._expect_ack = _yesno_to_bool(config['Poseidon']['EnableAcknowledgement'])
            self._encryption_enabled = _yesno_to_bool(config['Poseidon']['EnableEncyption'])
            self._encryption_keys = config['Poseidon']['EncryptionKey']

    def __set_config(self, attribute : str, value : str):
        config = ConfigParser(allow_no_value=True)
        config['Poseidon'] = {
            "OutputMode": self._output_mode,
            "EnableErrorCorrection": _bool_to_yesno(self._ecc_mode_enabled),
            "EnableAcknowledgement": _bool_to_yesno(self._expect_ack),
            "EnableEncyption": _bool_to_yesno(self._encryption_enabled),
            "EncryptionKey": self._encryption_keys
        }
        config["Poseidon"][attribute] = value
        with self.config_path.open("w") as fp:
            config.write(fp)

    ## output_mode/ OutputMode 
    @property
    def output_mode(self):
        return self._output_mode

    @output_mode.setter
    def output_mode(self, x):
        if x == "text" or x == "binary":
            self._output_mode = x
            self.__set_config(attribute="OutputMode", value=x)
        else:
            raise ValueError(f"Unsupported value: {x}, expecting text or binary")
        
    ## ecc_mode_enabled / EnableErrorCorrection
    @property
    def ecc_mode_enabled(self):
        return self._ecc_mode_enabled
    
    @ecc_mode_enabled.setter
    def ecc_mode_enabled(self, x):
        if type(x) == bool:
            self._ecc_mode_enabled = x
            self.__set_config(attribute="EnableErrorCorrection", value=_bool_to_yesno(x))
        else:
            raise ValueError(f"Unsupported value: {x}, expecting True or False")

    ## expect_ack / EnableAcknowledgement
    @property
    def expect_ack(self):
        return self._expect_ack
    
    @expect_ack.setter
    def expect_ack(self, x):
        if type(x) == bool:
            self._expect_ack = x
            self.__set_config(attribute="EnableAcknowledgement", value=_bool_to_yesno(x))
        else:
           raise ValueError(f"Unsupported value: {x}, expecting True or False") 

    ## encryption_enabled / EnableEncyption
    @property
    def encryption_enabled(self):
        return self._encryption_enabled
    
    @encryption_enabled.setter
    def encryption_enabled(self, x):
        if type(x) == bool:
            self._encryption_enabled = x
            self.__set_config(attribute="EnableEncyption", value=_bool_to_yesno(x))
        else:
            raise ValueError(f"Unsupported value: {x}, expecting True or False") 

    ## encryption_keys / EncryptionKey
    @property
    def encryption_keys(self):
        return self._encryption_keys
    
    @encryption_keys.setter
    def encryption_keys(self, x):
        if type(x) == str or x is None:
            self._encryption_keys = x
            self.__set_config(attribute="EncryptionKey", value=x)
        else:
            raise ValueError(f"Unsupported value: {x}, expecting string value or None")
    
def configuration_wizard(config : EmulatorConfiguration):
    # Detect keypresses, change configuration accordingly
    # v --> Text mode / Binary mode
    # b --> Error correction True/False
    # n --> Acknowledgement True/False
    # m --> Encryption True/False
    # e --> Set encryption key
    # Enter --> Start engine
    def _wizard_print_configuration(config: EmulatorConfiguration):
        clear()
        print("Poseidon Engine - Configuration / Launcher\n")
        print(f"Output Format: {config.output_mode} - [V]")
        print(f"Error correction: {config.ecc_mode_enabled} - [B]")
        print(f"Expect Ack Packets: {config.expect_ack} - [N]")
        print(f"Enable Encryption: {config.encryption_enabled} - [M]")
        print(f"Encryption Key: {config.encryption_keys} - Please edit poseidon_conf file\n")
        print("Press [Enter] to start the Poseidon Engine")
        print("Press [V], [B], [N], [M] to change the respective settings")

    def _handle_keypress(key):
        if key == Key.enter:
            return False
        else:
            try:
                if key.char == "v":
                    if config.output_mode == "text":
                        config.output_mode = "binary"
                    else:
                        config.output_mode = "text"
                    print("Changed output mode")
                elif key.char == "b":
                    if config.ecc_mode_enabled:
                        config.ecc_mode_enabled = False
                    else:
                        config.ecc_mode_enabled = True
                elif key.char == "n":
                    if config.expect_ack:
                        config.expect_ack = False
                    else:
                        config.expect_ack = True
                elif key.char == "m":
                    if config.encryption_enabled:
                        config.encryption_enabled = False
                    else:
                        config.encryption_enabled = True
                else:
                    pass
            except:
                pass
            _wizard_print_configuration(config)
    
    _wizard_print_configuration(config)
    with Listener(on_release=_handle_keypress) as listener:
        listener.join()

def main():
    c = Path("poseidon_conf")
    c.touch() # I'm gonna touch you
    conf = EmulatorConfiguration(c, True)
    conf.output_mode = "text"
    conf.ecc_mode_enabled = False
    conf.expect_ack = False
    conf.encryption_enabled = False
    conf.encryption_keys = None
    print(conf.output_mode, conf.ecc_mode_enabled, conf.expect_ack, conf.encryption_enabled, conf.encryption_keys)

if __name__ == "__main__":
    main()