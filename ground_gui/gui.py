# ------------------------------------------------------------------
# allows access to files in different folders
from sys import path
from os.path import abspath
CURRENT_PATH = abspath("")
if "ground_gui" in CURRENT_PATH:
    PATH_FRAMES = abspath("frames")
    PATH_HELPERS = abspath("helpers")
    logo_path = abspath("helios_logo.jpeg")
else:
    PATH_FRAMES = abspath("ground_gui/frames")
    PATH_HELPERS = abspath("ground_gui/helpers")
    logo_path = abspath("ground_gui/helios_logo.jpeg")
path.append(PATH_FRAMES)
path.append(PATH_HELPERS)
# ------------------------------------------------------------------

from window import window


if __name__ == "__main__":
    app = window("Helios", logo_path)
    app.mainloop()
