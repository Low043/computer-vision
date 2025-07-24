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

    def getTextFromFrame(self, frame: np.ndarray):
        try:
            # Pré-processamento da imagem
            croppedImg = frame[230:340, 250:580]
            blurImg = cv2.GaussianBlur(croppedImg, (5, 5), 0)

            # Imagem final e extração de texto
            finalImg = blurImg
            result = self.readtext(finalImg)

            cv2.imwrite(f'{self.saveFolder}/processed.png', finalImg)

            if not result:
                return 'Nenhum texto encontrado.'
            
            # Filtra os dígitos de todos os caracteres encontrados
            fullText = ''.join([res[1] for res in result])
            filteredText = re.sub(r'\D', '', fullText)

            return f'{filteredText} - {fullText}'
        
        except Exception as e:
            return f'Erro ao extrair texto: {e}'