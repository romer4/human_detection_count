from cv2 import threshold
import numpy as np
import uuid

from typing import Tuple
from attr import asdict
from math import sqrt

def get_center(box_coords: Tuple[float, float, float, float]) -> Tuple[float, float]:
    (x1, y1, x2, y2) = box_coords
    return ((x1 + x2) / 2, (y1 + y2) / 2)


class ObjectDetected:
    def __init__(self, id, box_coords: Tuple[float, float, float, float]) -> None:
        self.id = id
        self.box_coords = box_coords
        self.center_coords = get_center(box_coords)


    def set_coords(self, box_coords: Tuple[float, float, float, float]) -> None:
        self.box_coords = box_coords
        self.center_coords = get_center(box_coords)


class ObjectTracker:
    objects: ObjectDetected = []
    threshold = 10
    # def __init__(self, threshold: float) -> None:
    #     # self.objects: ObjectDetected = []
    #     self.threshold = threshold

    @staticmethod
    def track(x1: float, y1: float, x2: float, y2: float):
        print(len(ObjectTracker.objects))
        if (len(ObjectTracker.objects) == 0):
            newObject = ObjectTracker._create_object(x1, y1, x2, y2)
            ObjectTracker.objects.append(newObject)
            return newObject.id

        for key, object in enumerate(ObjectTracker.objects):
            (obj_x, obj_y) = object.center_coords
            (x, y) = get_center((x1, y1, x2, y2))
            distance = np.linalg.norm([[obj_x, obj_y], [x, y]])
            print(f"distance: {distance}")
            #if true, probably the object is the same as the checked
            if (distance <= ObjectTracker.threshold):
                ObjectTracker.objects[key].set_coords((x1, y1, x2, y2))
                return ObjectTracker.objects[key].id

        newObject = ObjectTracker._create_object(x1, y1, x2, y2)
        ObjectTracker.objects.append(newObject)
        return newObject.id

    @staticmethod
    def _create_object(x1: float, y1: float, x2: float, y2: float) -> ObjectDetected:
        object = ObjectDetected(uuid.uuid4(), (x1, y1, x2, y2))
        return object
