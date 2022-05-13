import cv2
import numpy as np
import ast
import easygui
from config_file_manager import load_file, save_file
from line_manager import LineManager, Orientation
from mouse_listener import MouseListener

image = np.zeros((500, 500, 3), np.uint8)
# image = "../data/p4.jpg"
open_helper_texts = True


def line_initiator() -> LineManager:
    line = LineManager(100, 250, 100, Orientation.VERTICAL)
    return line


def key_events(key):
    if (key & 0xff == 13):#enter
        line.save_line()
    elif (key & 0xff == ord("w")):
        line.toggle_orientation()
    elif (key & 0xff == ord("o")):
        open_image()
    elif (key & 0xff == ord("r")):
        line.reset()
    elif (key & 0xff == 192):
        global open_helper_texts
        open_helper_texts = not(open_helper_texts)
    # if (key & 0xff != 255): print(key & 0xff)


def helper_texts(frame):
    if (open_helper_texts):
        cv2.putText(frame, "(W) Mudar para horizontal/vertical", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "(R) Reseta a posicao da linha", (0, 25 * 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "(-> Enter) Salva as configuracoes da linha", (0, 25 * 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "(O) Abrir arquivos", (0, 25 * 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "(Q) Fechar programa", (0, 25 * 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "Mostrar menos (f3)", (0, 25 * 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    else:
        cv2.putText(frame, "Mostrar mais (f3)", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def open_image(*args):
    path = easygui.fileopenbox()
    global image
    image = path


def main():
    cv2.namedWindow("Line Manager")
    cv2.setMouseCallback("Line Manager", MouseListener.listener)
    cv2.createTrackbar("Comprimento da linha", "Line Manager", 100, 500, line.set_length)
    cv2.createButton("Vertical", line.set_orientation, None, cv2.QT_CHECKBOX, Orientation.VERTICAL)
    cv2.createButton("Salvar", line.save_line, None, cv2.QT_PUSH_BUTTON)
    cv2.createButton("Resetar", line.reset, None, cv2.QT_PUSH_BUTTON)
    cv2.createButton("Abrir imagem", open_image, None, cv2.QT_PUSH_BUTTON)
    while (1):
        print()
        if (isinstance(image, str)):
            blank_image = cv2.imread(image)
        else:
            blank_image = np.zeros((500, 500, 3), np.uint8)
        line.draw(blank_image)
        helper_texts(blank_image)
        cv2.imshow("Line Manager", blank_image)
        key = cv2.waitKey(1)
        key_events(key)
        if key & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    line = line_initiator()
    line.load_line()
    main()