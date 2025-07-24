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
            croppedImg = frame[220:350, 280:580]
            blurImg = cv2.GaussianBlur(croppedImg, (5, 5), 0)
            grayImg = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

            # Imagem final e extração de texto
            finalImg = grayImg
            result = self.readtext(finalImg)

            if saveFrame:
                cv2.imwrite(f'{self.saveFolder}/processed.png', finalImg)

            if not result:
                return 'Nenhum texto encontrado.'
            
            # Filtra os dígitos de todos os caracteres encontrados
            rawText = ''.join([res[1] for res in result])
            replacedText = rawText.replace('{', '1').replace('/', '1').replace('b', '8')
            fixedText = re.sub(r'\D', '', replacedText)

            return [fixedText, replacedText, rawText]
        
        except Exception as e:
            return f'Erro ao extrair texto: {e}'