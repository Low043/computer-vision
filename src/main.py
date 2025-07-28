"""Monitoramento da balança"""
import time
import os
import warnings
import base64
import requests
import dotenv
import cv2
from services.watcher import Watcher
from services.reader import Reader

# Ignora aviso do EasyOCR sobre pin_memory da GPU
warnings.filterwarnings('ignore', category = UserWarning, message = '.*pin_memory.*')

STREAM_URL = dotenv.get_key('.env', 'STREAM_URL')
SAVEFOLDER = 'src/images'

# Cria a pasta de imagens se não existir
os.makedirs(SAVEFOLDER, exist_ok = True)

watcher = Watcher(STREAM_URL, SAVEFOLDER)
reader = Reader(SAVEFOLDER)

while True:
    startTime = time.time()
    frame = watcher.get_frame()
    READOUT = reader.get_text_from_frame(frame, save_frame = True)

    ret, buffer = cv2.imencode('.jpg', frame)
    imgBase64 = base64.b64encode(buffer).decode('utf-8')

    endTime = time.time()

    print(f'Texto extraido: {READOUT} (Tempo: {endTime - startTime:.2f}s)')

    if  READOUT.isnumeric() and 800 < int(READOUT) < 5000:
        requests.post('http://localhost:3000', json = { 'image': imgBase64, 'weight': READOUT }, timeout = 300)
