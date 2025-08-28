"""Declaração da classe Watcher"""
from threading import Thread
import base64
import cv2

class Watcher:
    """Classe responsável por capturar frames da stream de vídeo em uma thread separada"""
    def __init__(self, stream_url):
        self.stream = cv2.VideoCapture(stream_url)
        _, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        """Inicia a execução da thread com a função update"""
        Thread(target=self.update, args=()).start()
        return self

    def stop(self):
        """Para a execução da thread"""
        self.stopped = True

    def get_frame(self):
        """Retorna o frame mais recente capturado do buffer"""
        return self.frame

    def update(self):
        """Lê continuamente os frames do buffer para atualizá-lo"""
        while not self.stopped:
            ok, frame = self.stream.read()
            if ok:
                self.frame = frame

    def ndarray_to_base64(self, image):
        """Converte uma imagem em formato ndarray para base64"""
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')

    def save_frame(self, frame, filename):
        """Salva o frame em um arquivo"""
        if frame is not None:
            cv2.imwrite(filename, frame)
