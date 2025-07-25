"""Monitoramento da balança"""
import time
import os
import warnings
import requests
import dotenv
from services.watcher import Watcher
from services.reader import Reader

# Ignora aviso do EasyOCR sobre pin_memory da GPU
warnings.filterwarnings('ignore', category = UserWarning, message = '.*pin_memory.*')

# Pega a URL do vídeo do arquivo .env
VIDEO_URL = dotenv.get_key('.env', 'VIDEO_URL')

# Cria a pasta de imagens se não existir
SAVEFOLDER = 'src/images'
os.makedirs(SAVEFOLDER, exist_ok = True)

watcher = Watcher(VIDEO_URL, SAVEFOLDER)
reader = Reader(SAVEFOLDER)

while True:
    startTime = time.time()
    frames = watcher.get_multiple_frames(1)
    stackedFrame = watcher.stack_frames(frames, save_frame = True)
    TEXTS = reader.get_text_from_frame(stackedFrame, save_frame = True)
    endTime = time.time()

    print(f'Texto extraido: {TEXTS} (Tempo: {endTime - startTime:.2f}s)')

    # requests.post('http://10.0.0.226:3000', json = { 'weight': TEXTS[0] }, timeout= 300)
