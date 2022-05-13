from pathlib import Path


DEFAULT_PATH = "../line.config"


def create_file():
    file = Path(DEFAULT_PATH)
    file.touch(exist_ok=True)
    return file


def save_file(line_manager):
    file = create_file()
    file.write_text(str(line_manager))
    return True


def load_file():
    file = create_file()
    text = file.read_text()
    return text