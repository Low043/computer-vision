"""Declaração da classe Watcher"""
import numpy as np
import cv2

class Watcher:
    """Classe que extrai e empilha frames da stream"""
    def __init__(self, stream_url: str, save_folder: str):
        self.stream_url = stream_url
        self.save_folder = save_folder

    def get_frame(self, save_frame: bool = False) -> list[np.ndarray]:
        """Extrai frames da stream"""
        cap = cv2.VideoCapture(self.stream_url)

        if not cap.isOpened():
            raise Exception('Erro ao abrir fonte de video.')

        _, frame = cap.read()

        cap.release()

        if save_frame:
            cv2.imwrite(f'{self.save_folder}/original.png', frame)

        return frame
