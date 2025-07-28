"""Declaração da classe Watcher"""
import os
import numpy as np
import cv2

class Watcher:
    """Classe que extrai e empilha frames da stream"""
    def __init__(self, stream_url: str, save_folder: str):
        self.stream_url = stream_url
        self.save_folder = os.path.abspath(save_folder)

    def get_multiple_frames(self, num_frames: int) -> list[np.ndarray]:
        """Extrai multiplos frames da stream de uma vez"""
        frames = []
        cap = cv2.VideoCapture(self.stream_url)

        if not cap.isOpened():
            raise Exception('Erro ao abrir fonte de vídeo.')

        for _ in range(num_frames):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()

        return frames

    def get_frame(self) -> list[np.ndarray]:
        """Extrai frames da stream"""
        cap = cv2.VideoCapture(self.stream_url)

        if not cap.isOpened():
            raise Exception('Erro ao abrir fonte de vídeo.')

        ret, frame = cap.read()

        cap.release()

        return frame

    def stack_frames(self, frames: list[np.ndarray], save_frame: bool = False):
        """Empilha os frames em uma imagem"""
        stacked_frame = np.mean(frames, axis=0).astype(np.uint8)
        if save_frame:
            cv2.imwrite(f'{self.save_folder}/stackedFrame.png', stacked_frame)

        return stacked_frame
