"""Monitoramento da balança"""
from services.watcher import Watcher, CamOfflineException
from services.reader import Reader
import time, os, base64, dotenv
from datetime import datetime
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
        self.process_id = os.getpid()

    def run(self):
        """Inicia o monitoramento da balança"""
        while True:
            start_time = time.time()
            try:
                frame = self.watcher.get_frame(save_frame = True)
                readout, original = self.reader.get_text_from_frame(frame, save_frame = True)
                image64 = self.image_to_base64(frame)
                end_time = time.time()
            except CamOfflineException as e:
                if self.cam_online:
                    self.change_camera_state(online = False)
                    print(f'Camera offline: {e}')
                continue
            except Exception as e:
                print(f'Erro ao processar o frame: {e}')
                continue

            if not self.cam_online:
                self.change_camera_state(online = True)

            print(f'Texto extraido: {readout} - {original} (Tempo: {end_time - start_time:.2f}s) (Timestamp: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')})')

            if readout.isnumeric() and 3000 <= int(readout) < 4000:
                self.send_message(image64, readout)
                print(f'Mensagem enviada, peso: {readout}')

    def send_message(self, image64, weight):
        """Envia a imagem e o peso para a API do WhatsApp"""
        message = f'⚠ALERTA DE EXCESSO DE PESO NO GUINCHO\n🕒Horário: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}\n🏗Peso detectado: {weight}kg\n🔴Situação: Valor lido excede o limite de 3.000 kg.\n📍Local: Área de Carga - Subsolo Extração 2 - Acesso B1\n👥Notificação enviada ao corpo técnico e supervisão\n❕Confirme o peso na imagem em anexo.'
        try:
            requests.post(self.api_url, json = { 'image': image64, 'weight': weight, 'message': message, 'pid': self.process_id }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

    def send_warning(self, message: str):
        """Envia um alerta para a API do WhatsApp"""
        try:
            requests.post(f'{self.api_url}/warning', json = { 'message': message, 'pid': self.process_id }, timeout = 300)
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
            print(f'✅ Alerta do sistema: Câmera online (Timestamp: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')})')
            # self.send_warning('✅ Alerta do sistema: Câmera online')
        else:
            print(f'🚫 Alerta do sistema: Câmera offline (Timestamp: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')})')
            # self.send_warning('🚫 Alerta do sistema: Câmera offline')

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
