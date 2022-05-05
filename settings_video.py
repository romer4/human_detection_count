import os.path
import cv2

def video_not_found(path):
    if not os.path.isfile(path):
        print("Vídeo não encontrado! @(")
        return


def video_condition(check):
    if not check:
        print("O arquivo não é um vídeo")
        return
    print("'Q' para sair")


def open_video(path):
    video_not_found(path)
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    video_condition(check)
    return video, check, frame
