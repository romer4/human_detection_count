from pathlib import Path
from line_manager import LineManager


DEFAULT_PATH = "../line.config"


def create_file():
    file = Path(DEFAULT_PATH)
    file.touch(exist_ok=True)
    return file


def save_file(line_manager: LineManager):
    file = create_file()
    # dictionary = {
    #     "orientation": 
    # }
    print(line_manager)
    file.write_text(str(line_manager))
    return True
