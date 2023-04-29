# ------------------------------------------------------------------
# allows access to files in different folders
from sys import path
from os.path import abspath
CURRENT_PATH = abspath("")
if "ground_gui" in CURRENT_PATH:
    PATH_FRAMES = f"{CURRENT_PATH}/frames"
    PATH_HELPERS = f"{CURRENT_PATH}/helpers"
    logo_path = f"{CURRENT_PATH}/helios_logo.jpeg"
else:
    PATH_FRAMES = f"{CURRENT_PATH}/ground_gui/frames"
    PATH_HELPERS = f"{CURRENT_PATH}/ground_gui/helpers"
    logo_path = f"{CURRENT_PATH}/ground_gui/helios_logo.jpeg"
path.append(PATH_FRAMES)
path.append(PATH_HELPERS)
# ------------------------------------------------------------------

from window import window


if __name__ == "__main__":
    app = window("Helios", logo_path)
    app.mainloop()
