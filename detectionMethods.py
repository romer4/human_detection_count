import cv2
import numpy as np
from colliders import lineCollider


net = cv2.dnn_DetectionModel(r"./datasets/frozen_inference_graph.pb", r"./datasets/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
with open("./datasets/coco.names", "rt") as file:
    CLASSES = file.read().rstrip("\n").split("\n")
def detectObjects(frame):
    acc = 0
    indexes, confidences, coords = net.detect(frame, confThreshold=0.5)
    if len(indexes) > 0:
        for index, confidence, coord in zip(indexes.flatten(), confidences.flatten(), coords):
            if CLASSES[index - 1] == "person":
                if lineCollider((coord[1] + coord[3]) * 2, 300, threshold=20):
                    acc += 1
                label = "{}: {:.2f}%".format(CLASSES[index - 1], confidence * 100)
                cv2.rectangle(frame, coord, color=(0, 255, 0))
                cv2.putText(frame, label, (coord[0] + coord[3], coord[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Frozen model detection", frame)
    return acc, frame

def yoloDetection(frame, threshold=0.5):
    # net = cv2.dnn.readNetFromDarknet("./datasets/yolo-coco/v4/yolov4.cfg", "./datasets/yolo-coco/v4/yolov4.weights")
    # net = cv2.dnn.readNetFromDarknet("./datasets/yolo-coco/yolov2-tiny.cfg", "./datasets/yolo-coco/yolov2-tiny.weights")
    # net = cv2.dnn.readNetFromDarknet("./datasets/yolo-coco/yolov3.cfg", "./datasets/yolo-coco/yolov3.weights")
    
    classes = open('./datasets/yolo-coco/coco.names').read().strip().split('\n')
    net = cv2.dnn.readNetFromDarknet("./datasets/yolo-coco/v4/yolov4-tiny.cfg", "./datasets/yolo-coco/v4/yolov4-tiny.weights")
    # net = cv2.dnn.readNetFromDarknet("./datasets/yolo-coco/v3-tiny/yolov3-tiny.cfg", "./datasets/yolo-coco/v3-tiny/yolov3-tiny.weights")
    # net = cv2.dnn.readNetFromONNX("./datasets/yolo-coco/v5/yolov5s.onnx")
    # net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    layerNames = net.getLayerNames()
    layerNames = [layerNames[(i - 1)[0]] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

    (h, w) = frame.shape[:2]

    net.setInput(blob)
    response = net.forward(layerNames)
    
    boxes = []
    confidences = []
    classesIndex = []
    classesNames = []

    for output in response:
        for detection in output:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence >= threshold:
                className = classes[classId]
                # if len(filters) == 0:
                #     box = detection[:4] * np.array([w, h, w, h])

                #     (cx, cy, width, height) = box.astype("int")
                #     x = int(cx - (width / 2))
                #     y = int(cy - (height / 2))

                #     box = [x, y, int(width), int(height)]

                #     boxes.append(box)
                #     confidences.append(float(confidence))
                #     classesIndex.append(classId)
                #     classesNames.append(className)
                if className == "person":
                    box = detection[:4] * np.array([w, h, w, h])

                    (cx, cy, width, height) = box.astype("int")
                    x = int(cx - (width / 2))
                    y = int(cy - (height / 2))

                    box = [x, y, int(width), int(height)]

                    boxes.append(box)
                    confidences.append(float(confidence))
                    classesIndex.append(classId)
                    # classesNames.append(className)
                    break
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    # coords = []
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y, w, h) = (boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
            (x1, y1) = (x + w, y + h)
            # coords.append((x, y, x1, y1))
            cv2.rectangle(frame, (x, y), (x1, y1), (255, 255, 255), 1)
            text = "{}: {:.4f}".format(classes[classesIndex[i]], confidences[i])
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (123, 0, 123), 1)
    cv2.imshow("yoloDetection", frame)
    return 0, frame
    