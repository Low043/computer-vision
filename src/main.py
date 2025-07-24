from services.ffmpeg import Watcher
from services.easyocr import Reader
import warnings
import dotenv
import os

# Ignora aviso do EasyOCR sobre pin_memory da GPU
warnings.filterwarnings('ignore', category = UserWarning, message = '.*pin_memory.*')

# Pega a URL do vídeo do arquivo .env
VIDEO_URL = dotenv.get_key('.env', 'VIDEO_URL')

# Cria a pasta de imagens se não existir
saveFolder = 'src/images'
os.makedirs(saveFolder, exist_ok = True)

watcher = Watcher(VIDEO_URL, saveFolder)
reader = Reader(saveFolder)

while True:
    frame = watcher.getCurrentFrame()
    text = reader.getTextFromFrame(frame)

    print(f'Texto extraido: {text}')