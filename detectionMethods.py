import cv2
from colliders import lineCollider


net = cv2.dnn_DetectionModel(r"./datasets/frozen_inference_graph.pb", r"./datasets/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def detectObjects(frame):
    acc = 0
    indexes, confidences, coords = net.detect(frame, confThreshold=0.5)
    
    if len(indexes) > 0:
        for index, confidence, coord in zip(indexes.flatten(), confidences.flatten(), coords):
            if index == 1:
                if lineCollider((coord[1] + coord[3]) * 2, 300, threshold=20):
                    acc += 1
                label = "{}: {:.2f}%".format("person", confidence * 100)
                cv2.rectangle(frame, coord, color=(0, 255, 0))
                cv2.putText(frame, label, (coord[0] + coord[3], coord[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Frozen model detection", frame)
    return acc, frame