import cv2
import imutils
import os.path

from settings_video import open_video
from datetime import datetime
from detectionMethods import detectObjects

class MethodsOutput:
    def __init__(self, path: str, width: int=750) -> None:
        self.path = path
        self.detector = detectObjects
        self.width = width

 
    def video(self):
        writer = cv2.VideoWriter(r"./data_output/output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 1, (600,600))
        video, check, frame = open_video(self.path)

        lastTime = datetime.timestamp(datetime.now())
        initial_time = datetime.timestamp(datetime.now())
        frames_amount = 0
        totalPersons = 0

        while video.isOpened():
            frames_amount += 1
            check, frame = video.read()
            if check:
                currentTime = datetime.timestamp(datetime.now())
                delta = (currentTime - lastTime)
                lastTime = currentTime
                fps = int(1 / delta)
                cv2.line(frame, (0, 150-30), (self.width, 150-30), (0, 0, 0), 1)
                cv2.line(frame, (0, 150), (self.width, 150), (0, 255, 0), 1)
                cv2.line(frame, (0, 150+30), (self.width, 150+30), (255, 0, 0), 1)
                cv2.putText(frame, f"Pessoas: {totalPersons}", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "FPS: {}".format(fps), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, f"{round(delta * 1000, 2)}ms", (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                frame = imutils.resize(frame, width=min(self.width, frame.shape[1]))
                count, frame = self.detector(frame)

                totalPersons += count

                if writer is not None:
                    writer.write(frame)

                if cv2.waitKey(1) & 0xff == ord("q"):
                    print("Quitting")
                    break
            else:
                break
        
        video.release()

        end_time = datetime.timestamp(datetime.now())
        delta = end_time - initial_time
        print("média de frames")
        print(frames_amount / delta)
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
