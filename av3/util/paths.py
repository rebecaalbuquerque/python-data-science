from pathlib import Path
import platform

separator = "\\"

if platform.system() == "Darwin":
    separator = "/"

path_input_data = str(Path().absolute().parent.parent) + separator + "energydados" + separator + "input" + separator
path_output_data = str(Path().absolute().parent.parent) + separator + "energydados" + separator + "output" + separator

