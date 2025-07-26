"""Declaração da classe Watcher"""
import numpy as np
import cv2
import os

class Watcher:
    """Classe que extrai e empilha frames da stream"""
    def __init__(self, stream_url: str, save_folder: str):
        self.stream_url = os.path.abspath(stream_url)
        self.save_folder = os.path.abspath(save_folder)

    def get_multiple_frames(self, num_frames: int) -> list[np.ndarray]:
        """Extrai frames da stream"""
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
    
    def get_frame_by_index(self, index: int) -> np.ndarray:
        cap = cv2.VideoCapture(self.stream_url)

        if not cap.isOpened():
            raise Exception('Erro ao abrir fonte de vídeo.')

        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

        ret, frame = cap.read()

        cap.release()
        return frame

    def stack_frames(self, frames: list[np.ndarray], save_frame: bool = False):
        """Empilha os frames em uma imagem"""
        stacked_frame = np.mean(frames, axis=0).astype(np.uint8)
        if save_frame:
            cv2.imwrite(f'{self.save_folder}/stackedFrame.png', stacked_frame)

        return stacked_frame
