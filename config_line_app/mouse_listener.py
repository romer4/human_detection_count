import cv2


class MouseListener:
    x: int = 0
    y: int = 0
    is_holding = False

    @staticmethod
    def listener(event, x, y, flags, param):
        MouseListener.x = x
        MouseListener.y = y
        if (event == cv2.EVENT_LBUTTONDOWN):
            MouseListener.is_holding = True
        elif (event == cv2.EVENT_LBUTTONUP):
            MouseListener.is_holding = False
