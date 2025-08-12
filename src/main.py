"""Monitoramento da balança"""
from services.watcher import Watcher
from services.reader import Reader
import time, os, base64, dotenv
import requests
import warnings
import cv2

# Ignora aviso do EasyOCR sobre pin_memory da GPU
warnings.filterwarnings('ignore', category = UserWarning, message = '.*pin_memory.*')

class Monitoring:
    """Classe que monitora a balança e envia os dados para a API do WhatsApp"""
    def __init__(self, stream_url: str, api_url: str, save_folder: str):
        self.watcher = Watcher(stream_url, save_folder)
        self.reader = Reader(save_folder)
        self.api_url = api_url

    def run(self):
        """Inicia o monitoramento da balança"""
        while True:

            start_time = time.time()
            try:
                frame = self.watcher.get_frame(save_frame = True)
                readout, original = self.reader.get_text_from_frame(frame, save_frame = True)
                image64 = self.image_to_base64(frame)
            except Exception as e:
                print(f'Erro ao processar o frame: {e}')
                continue
            end_time = time.time()

            print(f'Texto extraido: {readout} - {original} (Tempo: {end_time - start_time:.2f}s)')

            if readout.isnumeric() and 3000 <= int(readout) < 4000:
                self.send_message(image64, readout)
                print(f'Mensagem enviada, peso: {readout}')

    def send_message(self, image64, weight):
        """Envia a imagem e o peso para a API do WhatsApp"""
        try:
            requests.post(self.api_url, json = { 'image': image64, 'weight': weight }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

    def image_to_base64(self, image):
        """Converte uma imagem OpenCV para base64"""
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')

if __name__ == '__main__':
    dotenv.load_dotenv()

    STREAM_URL = os.getenv('STREAM_URL')
    API_URL = os.getenv('API_URL')
    SAVEFOLDER = 'src/images'

    # Cria a pasta de imagens se não existir
    os.makedirs(SAVEFOLDER, exist_ok = True)

    # Inicia o monitoramento
    monitoring = Monitoring(STREAM_URL, API_URL, SAVEFOLDER)
    monitoring.run()
