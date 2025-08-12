"""Monitoramento da balança"""
from services.watcher import Watcher, CamOfflineException
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
        self.cam_online = True

    def run(self):
        """Inicia o monitoramento da balança"""
        while True:
            start_time = time.time()
            try:
                frame = self.watcher.get_frame(save_frame = True)
                readout, original = self.reader.get_text_from_frame(frame, save_frame = True)
                image64 = self.image_to_base64(frame)
            except CamOfflineException as e:
                if self.cam_online:
                    self.change_camera_state(online = False)
                continue
            except Exception as e:
                print(f'Erro ao processar o frame: {e}')
                continue
            end_time = time.time()

            if not self.cam_online:
                self.change_camera_state(online = True)

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

    def send_warning(self, message: str):
        """Envia um alerta para a API do WhatsApp"""
        try:
            requests.post(f'{self.api_url}/warning', json = { 'message': message }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar aviso: {e}')

    def image_to_base64(self, image):
        """Converte uma imagem OpenCV para base64"""
        _, buffer = cv2.imencode('.jpg', image)
        return base64.b64encode(buffer).decode('utf-8')
    
    def change_camera_state(self, online: bool):
        """Altera o estado da câmera (online/offline)"""
        self.cam_online = online
        status = 'online' if online else 'offline'
        print(f'Camera {status}')

        if online:
            self.send_warning('✅ Alerta do sistema: Câmera online')
        else:
            self.send_warning('🚫 Alerta do sistema: Câmera offline')

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
