"""Declaração da classe Reader"""
import numpy as np
import easyocr
import cv2
import re

class Reader(easyocr.Reader):
    """Classe que lê texto de uma imagem"""
    def __init__(self, save_folder: str):
        print('Iniciando leitor OCR...')

        super().__init__(['pt'], gpu = False, verbose = False)
        self.save_folder = save_folder

        print('Leitor OCR iniciado com sucesso!')

    def get_text_from_frame(self, frame: np.ndarray, save_frame: bool = False):
        """Pré-processa a imagem, e extrai o texto usando o easyOCR"""
        try:
            cropped_img = frame[220:360, 280:580]
            blur_img = cv2.GaussianBlur(cropped_img, (5, 5), 0)
            gray_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
            threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 19, 3)


            final_img = threshold_img

            if save_frame:
                cv2.imwrite(f'{self.save_folder}/processed.png', final_img)

            result = self.readtext(final_img, allowlist='0123456789')
            text = ''.join([res[1] for res in result])

            return text  

        except Exception as e:
            return f'Erro ao extrair texto: {e}'

    def to_threshold(self, img: np.ndarray):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fimg = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 1)
        cv2.imwrite('src/images/thresholded.png', fimg)

