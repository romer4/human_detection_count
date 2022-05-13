import ast
from typing import Tuple, Union
from cv2 import log
from numpy import ndarray
from enum import IntEnum
import cv2
from config_file_manager import load_file, save_file

from mouse_listener import MouseListener


class Orientation(IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class LineManager:

    def __init__(self, x: int, y: int, length: int, orientation: Orientation=Orientation.HORIZONTAL, color: Tuple[int, int, int]=(0, 255, 0), thickness: int=1, threshold: int=5) -> None:
        self.x = x
        self.y = y
        self.length = length
        self.orientation: Orientation = orientation
        self.color = color
        self.thickness = thickness
        self.threshold = threshold
        self.is_grabbing = False


    def __str__(self):
        dict = {
            "orientation": int(self.orientation),
            "x": self.x,
            "y": self.y,
            "threshold": self.threshold
        }
        return f"{dict}"


    def draw(self, frame: ndarray):

        mouse_x, mouse_y = MouseListener.x, MouseListener.y

        if (MouseListener.is_holding and self.__pos_inside_box((mouse_x, mouse_y))): self.is_grabbing = True
        elif (not MouseListener.is_holding): self.is_grabbing = False
        
        if (self.is_grabbing):
            if (self.orientation == Orientation.HORIZONTAL):
                self.x = int(mouse_x - self.length / 2)
                self.y = mouse_y
            elif (self.orientation == Orientation.VERTICAL):    
                self.x = mouse_x
                self.y = int(mouse_y - self.length / 2)

        if (self.orientation == Orientation.HORIZONTAL):
            cv2.line(frame, (self.x, self.y), (self.x + self.length, self.y), self.color, self.thickness)
        elif (self.orientation == Orientation.VERTICAL):
            cv2.line(frame, (self.x, self.y), (self.x, self.y + self.length), self.color, self.thickness)


    def set_length(self, length):
        self.length = length


    def set_orientation(self, orientation, _):
        if (orientation == 0): self.orientation = Orientation.HORIZONTAL
        elif (orientation == 1): self.orientation = Orientation.VERTICAL


    def toggle_orientation(self):
        if (self.orientation == Orientation.HORIZONTAL): self.orientation = Orientation.VERTICAL
        elif (self.orientation == Orientation.VERTICAL): self.orientation = Orientation.HORIZONTAL


    def save_line(self, *args):
        save_file(self)


    def load_line(self):
        try:
            file = ast.literal_eval(load_file())
        except ValueError:
            print("Arquivo de salvamento está com algo errado e não pode ser lido")
        except SyntaxError:
            print("Arquivo de salvamento está com algo errado e não pode ser lido")
        except:
            print("Falha ao carregar o salvamento anterior da linha")
        finally:
            self.orientation = file["orientation"]
            self.x = file["x"]
            self.y = file["y"]
            self.threshold = file["threshold"]


    def reset(self, *args):
        self.x = 250
        self.y = 250


    def __get_collider_box(self) -> Tuple[int, int, int, int]:
        if (self.orientation == Orientation.HORIZONTAL):
            y1 = self.y + self.threshold
            y2 = self.y - self.threshold
            x1 = self.x
            x2 = self.x + self.length
            return (x1, y1, x2, y2)
        elif (self.orientation == Orientation.VERTICAL):
            y1 = self.y
            y2 = self.y + self.length
            x1 = self.x - self.threshold
            x2 = self.x + self.threshold
            return (x1, y1, x2, y2)


    def __pos_inside_box(self, coord: Tuple[int, int]) -> bool:
        """Checks if a point passed is inside the line box, it's like a collider"""
        x, y = coord
        x1, y1, x2, y2 = self.__get_collider_box()
    
        if (self.orientation == Orientation.HORIZONTAL):
            if (x >= x1 and x <= x2 and y <= y1 and y >= y2): return True
        elif (self.orientation == Orientation.VERTICAL):
            if (x >= x1 and x <= x2 and y >= y1 and y <= y2): return True
        return False
