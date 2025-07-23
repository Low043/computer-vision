import easyocr
import cv2
import re
import os

# Cria a pasta de imagens processadas se não existir
os.makedirs('images/processed', exist_ok = True)

print('Iniciando leitor OCR...')
reader = easyocr.Reader(['pt'], gpu = False, verbose = False)
print('Leitor OCR iniciado com sucesso!')

def getTextFromImg(imagePath: str):
    try:
        img = cv2.imread(imagePath)

        # Pré-processamento da imagem
        croppedImg = img[230:340, 250:580]
        blurImg = cv2.GaussianBlur(croppedImg, (5, 5), 0)

        # Imagem final e extração de texto
        finalImg = blurImg
        result = reader.readtext(finalImg)

        # Salva a imagem final processada
        imgName = imagePath.split('/')[-1]
        cv2.imwrite(f'images/processed/{imgName}', finalImg)

        if not result:
            return 'Nenhum texto encontrado.'
        
        # Filtra os dígitos de todos os caracteres encontrados
        fullText = ''.join([res[1] for res in result])
        filteredText = re.sub(r'\D', '', fullText)

        return filteredText
    
    except FileNotFoundError:
        return f'Erro: O arquivo {imagePath} não foi encontrado.'
    except Exception as e:
        return f'Ocorreu um erro inesperado: {e}'


for i in range(4):
    result = getTextFromImg(f'images/teste{i+1}.png')
    print(f'Numero extraido da imagem {i+1}: {result}')