import cv2
import numpy as np
from config_file_manager import save_file
from line_manager import LineManager, Orientation
from mouse_listener import MouseListener


BLANK_IMAGE = np.zeros((500, 500, 3), np.uint8)

def line_initiator() -> LineManager:
    line = LineManager(100, 250, 100, Orientation.VERTICAL)
    return line


line = line_initiator()


def save_line(_, __):
    save_file(line)


def main():
    cv2.namedWindow("Line Manager")
    cv2.setMouseCallback("Line Manager", MouseListener.listener)
    cv2.createTrackbar("length", "Line Manager", 0, 500, line.set_length)
    cv2.createButton("Vertical", line.set_orientation, None, cv2.QT_CHECKBOX, Orientation.VERTICAL)
    cv2.createButton("Salvar", save_line, None, cv2.QT_PUSH_BUTTON)
    while (1):
        blank_image = np.zeros((500, 500, 3), np.uint8)
        line.draw(blank_image)
        cv2.imshow("Line Manager", blank_image)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()