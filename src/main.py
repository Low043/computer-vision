"""Monitoramento da balança"""
import time
import os
import warnings
from services.watcher import Watcher
from services.reader import Reader

# Ignora aviso do EasyOCR sobre pin_memory da GPU
warnings.filterwarnings('ignore', category = UserWarning, message = '.*pin_memory.*')

VIDEO_URL = 'src/input/gravacao_camera0.mkv'
SAVEFOLDER = 'src/images'
ITERATION = 0

# Cria a pasta de imagens se não existir
os.makedirs(SAVEFOLDER, exist_ok = True)

watcher = Watcher(VIDEO_URL, SAVEFOLDER)
reader = Reader(SAVEFOLDER)

while True:
    startTime = time.time()

    frame = watcher.get_frame_by_index(ITERATION)

    TEXTS = reader.get_text_from_frame(frame, save_frame = True)
    endTime = time.time()

    print(f'Texto extraido: {TEXTS} (Tempo: {endTime - startTime:.2f}s; Frame: {ITERATION})')
    ITERATION += 1
