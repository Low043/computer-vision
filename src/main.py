from services.watcher import Watcher
from services.reader import Reader
import requests
import warnings
import dotenv
import time
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
    startTime = time.time()
    frames = watcher.getMultipleFrames(10)
    stackedFrame = watcher.stackFrames(frames, saveFrame = True)
    texts = reader.getTextFromFrame(stackedFrame, saveFrame = True)
    endTime = time.time()

    print(f'Texto extraido: {texts} (Tempo: {endTime - startTime:.2f}s)')

    requests.post('http://10.0.0.226:3000', json = { 'weight': texts[0] })