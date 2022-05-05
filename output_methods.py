import cv2
import imutils
import os.path

from settings_video import open_video
from datetime import datetime
from detectionMethods import detectObjects


class Methods_output:
    def __init__(self, path) -> None:
        self.path = path
        self.detector = detectObjects


    def image(self, known_image_path=None):
        if not os.path.isfile(self.path):
            print("Imagem não encontrada! @(")
            return

        frame = cv2.imread(self.path)
        frame = imutils.resize(frame, width=min(320, frame.shape[1]))

        if known_image_path: 
            known_image_frame = cv2.imread(known_image_path)
            self.detector(frame, known_image_frame, True)
        else: self.detector(frame)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getVideoFrame(self, writer, known_image_path=None, catch_frame=0):
        video, _, frame = open_video(self.path)

        curr_frame = 0
        while video.isOpened():
            if curr_frame == catch_frame: break
            _, frame = video.read()
            curr_frame += 1
            if writer is not None:
                writer.write(frame)

        frame = imutils.resize(frame, width=min(320, frame.shape[1]))

        if known_image_path:
            known_image_frame = cv2.imread(known_image_path)
            self.detector(frame, known_image_frame, True)
        else:
            self.detector(frame)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
 
    def video(self):
        writer = cv2.VideoWriter(r"./data_output/output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 1, (600,600))
        video, check, frame = open_video(self.path)

        lastTime = datetime.timestamp(datetime.now())
        ant = 0
        totalPersons = 0
        while video.isOpened():
            check, frame = video.read()
            if check:
                currentTime = datetime.timestamp(datetime.now())
                delta = (currentTime - lastTime)
                lastTime = currentTime
                fps = int(1 / delta)
                cv2.line(frame, (0, 150), (750, 150), (0, 255, 0), 1)
                cv2.putText(frame, f"Pessoas: {totalPersons}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "FPS: {}".format(fps), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, f"{round(delta * 1000, 2)}ms", (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                frame = imutils.resize(frame, width=min(750, frame.shape[1]))
                count, frame = self.detector(frame)

                if count > ant:
                    totalPersons += 1
            
                ant = count
                if writer is not None:
                    writer.write(frame)

                if cv2.waitKey(1) & 0xff == ord("q"):
                    print("Quitting")
                    break
            else:
                break
        
        video.release()
        cv2.destroyAllWindows()

    def camera(self): 
        writer = cv2.VideoWriter(r"./data_output/output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 1, (600,600))  
        video = cv2.VideoCapture(0)
        ant = 0
        totalPersons = 0
        while True:
            _, frame = video.read()
            count, frame = self.detector(frame)
            #count numero p tela

            if count > ant:
                totalPersons += 1
            
            ant = count

            # cv2.putText(frame, "Pessoas: {}".format(totalPersons), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            print(totalPersons)
            if writer is not None:
                writer.write(frame)

            if cv2.waitKey(1) & 0xff == ord("q"):
                break
            
        video.release()
        cv2.destroyAllWindows()
