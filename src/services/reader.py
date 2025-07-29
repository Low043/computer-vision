"""Declaração da classe Reader"""
import numpy as np
import easyocr
import cv2
from . import imgProcesing

class Reader(easyocr.Reader):
    """Classe que lê texto de uma imagem"""
    def __init__(self, save_folder: str):
        print('Iniciando leitor OCR...')

        super().__init__(['pt'], gpu = False, verbose = False)
        self.img_processor = imgProcesing.ImgProcessing()
        self.save_folder = save_folder

        print('Leitor OCR iniciado com sucesso!')

    def get_text_from_frame(self, frame: np.ndarray, save_frame: bool = False):
        """Pré-processa a imagem, e extrai o texto usando o easyOCR"""
        try:
            actions = {
                'crop': [220, 350, 340, 565],
                'rgb_to_gray': True,
                'threshold': True
            }

            processed_img = self.img_processor.execute(actions, frame)

            final_img = processed_img

            if save_frame:
                cv2.imwrite(f'{self.save_folder}/processed.png', final_img)

            result = self.readtext(final_img, allowlist='0123456789')
            text = ''.join([res[1] for res in result])

            return text

        except Exception as e:
            return f'Erro ao extrair texto: {e}'
