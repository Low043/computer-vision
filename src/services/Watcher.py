import cv2

class Watcher:
    def __init__(self, stream_url: str, save_folder: str):
        self.stream_url = stream_url
        self.save_folder = save_folder

    def get_frame(self, save_frame: bool = False):
        cap = cv2.VideoCapture(self.stream_url)

        if not cap.isOpened():
            raise CamOfflineException('Erro ao abrir fonte de video')

        _, frame = cap.read()

        cap.release()

        if save_frame:
            cv2.imwrite(f'{self.save_folder}/original.png', frame)

        return frame

class CamOfflineException(Exception):
    pass