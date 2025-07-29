"""Declaração da classe Reader"""
import numpy as np
import easyocr
import cv2

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
            final_img = self.preprocessing_img(frame)

            if save_frame:
                cv2.imwrite(f'{self.save_folder}/processed.png', final_img)

            result = self.readtext(final_img, allowlist='0123456789')

            return self.accurate_text(result)

        except Exception as e:
            return f'Erro ao extrair texto: {e}'

    def preprocessing_img(self, image: np.ndarray):
        """Pré-processa a imagem para melhorar a leitura OCR"""
        cropped_img = image[220:350, 340:565]
        blur_img = cv2.GaussianBlur(cropped_img, (5, 5), 0)
        gray_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 37, 7)

        return threshold_img

    def accurate_text(self, read_result: list[str]):
        """Processa o resultado do OCR em um texto mais preciso"""
        original_text = ''.join([res[1] for res in read_result])
        text = original_text

        if len(text) > 3:
            if text[:2] == '88' or text[:2] == '44' or text[:2] == '77':
                text = '11' + text[2:]
            if text[0] == '8' or text[0] == '4' or text[0] == '7':
                text = '1' + text[1:]
            if text[1] == '4':
                text = text[0] + '1' + text[2:]
            if text[1] == '8':
                text = text[0] + '0' + text[2:]

        return [text, original_text]