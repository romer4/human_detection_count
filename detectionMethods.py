import cv2

from colliders import lineCollider
from object_tracking import ObjectTracker, get_center

net = cv2.dnn_DetectionModel(r"./datasets/frozen_inference_graph.pb", r"./datasets/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def detectObjects(frame, threshold=0.5):
    acc = 0
    indexes, confidences, coords = net.detect(frame, confThreshold=threshold)
    ObjectTracker.update()
    if len(indexes) > 0:
        for index, confidence, coord in zip(indexes.flatten(), confidences.flatten(), coords):
            if index == 1:#index == 1 is person
                x1, y1, w, h = coord
                x2, y2 = x1 + w, y1 + h
                center = get_center((x1, y1, x2, y2))
                obj = ObjectTracker.track(center[0], center[1])
                id = obj.id

                if lineCollider(center[1], 150, threshold=30) and obj.has_passed_line == False:
                    print("line collided")
                    obj.has_passed_line = True
                    #if the first y are less than the half of the screen => coming from above, otherwise it's coming from below
                    if (obj.original_coords[1] < frame.shape[1] / 2): acc += 1
                    else: acc -= 1
                label = "{}: {:.2f}%".format("Person", confidence * 100)

                cv2.circle(frame, (int(center[0]), int(center[1])), radius=3, color=(0, 0, 255), thickness=-1)
                cv2.rectangle(frame, coord, color=(0, 255, 0))
                cv2.putText(frame, label, (x2 + 10, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, f"id: {id}", (x2 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Frozen model detection", frame)
    return acc, frame
