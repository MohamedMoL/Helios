# ------------------------------------------------------------------
# allows access to files in different folders
from sys import path
from os.path import abspath
PATH_FRAMES = abspath("ground_gui/frames")
PATH_HELPERS = abspath("ground_gui/helpers")
path.append(PATH_FRAMES)
path.append(PATH_HELPERS)
# ------------------------------------------------------------------

from window import window


if __name__ == "__main__":
    app = window("Helios")
    app.mainloop()
