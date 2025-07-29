"""Declaração de classe de Processamento de Imagem"""
import numpy as np
import cv2

class ImgProcessing:
    """Classe responsável pelo processamento de imagens"""
    def __init__(self):
        pass

    def crop(self, img: np.ndarray, coordinates: list) -> np.ndarray:
        """Corta a imagem de acordo com as coordenadas fornecidas"""
        y1, y2, x1, x2 = coordinates
        processed_img = img[y1:y2, x1:x2]
        return processed_img

    def rgb_to_gray(self, img: np.ndarray) -> np.ndarray:
        """Converte uma imagem BGR para escala de cinza"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def threshold(self, img: np.ndarray) -> np.ndarray:
        """Aplica um threshold adaptativo na imagem"""
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 37, 7)

    def execute(self, actions: dict, img: np.ndarray) -> np.ndarray:
        """Executa as ações de processamento de imagem todas de uma vez"""
        if actions['crop'] is not None:
            processed_img = self.crop(actions['crop'], img)
            img = processed_img

        if actions['rgb_to_gray'] is not None:
            processed_img = self.rgb_to_gray(img)
            img = processed_img

        if actions['threshold'] is not None:
            processed_img = self.threshold(img)
            img = processed_img

        return img
