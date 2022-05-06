from datetime import datetime

DEFAULT_LOG_PATH = ".log"

def log(message):
    file = open(DEFAULT_LOG_PATH, "a")
    file.write("\n")
    file.write("{}: {}".format(datetime.now(), message))
    file.close()

def clear():
    file = open(DEFAULT_LOG_PATH, "w")
    file.write("")
    file.close()
