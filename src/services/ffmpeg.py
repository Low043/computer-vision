import numpy as np
import subprocess
import cv2

class Watcher:
    def __init__(self, streamUrl: str, saveFolder: str):
        self.streamUrl = streamUrl
        self.saveFolder = saveFolder

    def getCurrentFrame(self) -> np.ndarray:
        command = [
            'ffmpeg',
            '-i', self.streamUrl,
            '-frames:v', '1',
            '-f', 'image2pipe',
            '-vcodec', 'png',
            '-'
        ]

        try:
            pipe = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)
            image_bytes = np.frombuffer(pipe.stdout, dtype = np.uint8)
            frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

            cv2.imwrite(f'{self.saveFolder}/frame.png', frame)

            return frame

        except Exception as e:
            return f'Erro ao extrair frame: {e}'