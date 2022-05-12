import numpy as np
import uuid

from typing import Tuple, List

from log import log

def get_center(box_coords: Tuple[float, float, float, float]) -> Tuple[float, float]:
    (x1, y1, x2, y2) = box_coords
    return ((x1 + x2) / 2, (y1 + y2) / 2)


class ObjectDetected:
    """
    Holds a detected person or any other object based on its current coords and previous coords
    """
    def __init__(self, id, coords: Tuple[float, float]) -> None:
        self.id = id
        self.coords = coords
        self.has_passed_line = False
        self.original_coords = coords
        self.tick = 0


    def set_coords(self, coords: Tuple[float, float]) -> None:
        self.coords = coords


class ObjectTracker:
    """
    Has a list of objects detecteds and methods for verifications and validations for the objects
    """
    objects: List[ObjectDetected] = []
    threshold = 15
    max_tick = 10

    @staticmethod
    def track(x: float, y: float):
        print(f"length: {len(ObjectTracker.objects)}")
        if (len(ObjectTracker.objects) == 0):
            #creating a new object if there isn't any to compare
            new_object = ObjectTracker._create_object(x, y)
            ObjectTracker.objects.append(new_object)
            return new_object

        for object in ObjectTracker.objects:
            (obj_x, obj_y) = object.coords
            obj_array = np.array(obj_x, obj_y)
            curr_coords_array = np.array(x, y)
            #getting the distance between two points (object coords and current frame coords)
            distance = np.linalg.norm(obj_array - curr_coords_array)

            #if true, probably the object is the same as the checked
            #is detected as a previous object
            if (distance <= ObjectTracker.threshold):
                object.set_coords((x, y))
                object.tick = 0
                return object

        #if any object is found in the loop, we create a new object
        new_object = ObjectTracker._create_object(x, y)
        ObjectTracker.objects.append(new_object)
        return new_object

    @staticmethod
    def _create_object(x: float, y: float) -> ObjectDetected:
        object = ObjectDetected(uuid.uuid4(), (x, y))
        return object

    
    @staticmethod
    def find(id: str) -> ObjectDetected:
        return [object for object in ObjectTracker.objects if object.id == id][0]


    @staticmethod
    def update() -> None:
        def remove_object(key, object):
            if (object.tick >= ObjectTracker.max_tick):
                ObjectTracker.objects.pop(key)
            object.tick += 1
        [remove_object(key, object) for key, object in enumerate(ObjectTracker.objects)]
