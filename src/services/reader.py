import numpy as np
import easyocr
import cv2
import re
    
class Reader(easyocr.Reader):
    def __init__(self, saveFolder: str):
        print('Iniciando leitor OCR...')

        super().__init__(['pt'], gpu = False, verbose = False)
        self.saveFolder = saveFolder

        print('Leitor OCR iniciado com sucesso!')

    def getTextFromFrame(self, frame: np.ndarray, saveFrame: bool = False):
        try:
            # Pré-processamento da imagem
            croppedImg = frame[220:360, 280:580]
            blurImg = cv2.GaussianBlur(croppedImg, (5, 5), 0)
            grayImg = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

            finalImg = grayImg

            if saveFrame:
                cv2.imwrite(f'{self.saveFolder}/processed.png', finalImg)

            result = self.readtext(finalImg, allowlist='0123456789')
            text = ''.join([res[1] for res in result])

            return text
        
        except Exception as e:
            return f'Erro ao extrair texto: {e}'