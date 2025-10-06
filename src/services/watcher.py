"""Declaração da classe Watcher"""
from threading import Thread
import time
import cv2

class Watcher:
    """Classe responsável por capturar frames da stream de vídeo em uma thread separada"""
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.previous_connected = False # Usado para detectar mudanças no estado de conexão
        self.connected = False
        self.stopped = False
        self.stream = None
        self.frame = None

        self.handle_connection()

    def start(self):
        """Inicia a execução da thread com a função update"""
        Thread(target=self.update, args=()).start()
        return self

    def stop(self):
        """Para a execução da thread"""
        self.stopped = True

    def update(self):
        """Lê continuamente os frames do buffer para atualizá-lo"""
        while not self.stopped:
            self.handle_connection()
            if not self.connected:
                continue
            
            ok, frame = self.stream.read()
            if ok:
                self.frame = frame

    def get_frame(self):
        """Retorna o frame mais recente capturado do buffer"""
        return self.frame

    def save_frame(self, frame, filename):
        """Salva o frame em um arquivo"""
        if frame is not None:
            cv2.imwrite(filename, frame)

    def handle_connection(self):
        if self.connected != self.previous_connected:
            self.previous_connected = self.connected
            if self.connected:
                print('Conexão com a stream estabelecida')
            else:
                print('Tentando reconectar à stream...')

        if not self.connected:
            self.stream = cv2.VideoCapture(self.stream_url)
            self.connected = self.stream.isOpened()
            if not self.connected:
                time.sleep(5) # Espera 5 segundos antes de tentar reconectar
