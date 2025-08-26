"""Orquestra a execução do app"""
import time
from datetime import datetime
import os
import requests
import dotenv
from services.watcher import Watcher
from services.reader import Reader

STREAM_URL = dotenv.get_key(dotenv.find_dotenv(), 'STREAM_URL')
API_URL = dotenv.get_key(dotenv.find_dotenv(), 'API_URL')

class Monitoring:
    """Classe responsável pela lógica do monitoramento da stream"""
    def __init__(self, stream_url, api_url):
        self.watcher = Watcher(stream_url).start()
        self.reader = Reader()
        self.delay = 1
        self.process_id = os.getpid()
        self.api_url = api_url

    def start(self):
        """Inicia o monitoramento da stream"""
        try:
            self.__main_loop()
        finally:
            self.watcher.stop()

    def __main_loop(self):
        while True:
            time.sleep(self.delay)
            start_time = time.time()
            
            frame = self.watcher.get_frame()
            [result, image] = self.reader.get_frame_text(frame)

            end_time = time.time()
            processing_time = end_time - start_time

            print(f'Texto extraido: {result} (Processing Time: {processing_time:.2f}s) (Timestamp: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')})')

            try:
                if 3000 <= int(result) < 4000:
                    image64 = self.watcher.ndarray_to_base64(image)
                    self.send_message(image64, result)
                    print(f'Peso detectado: {result}kg - Mensagem enviada.')
            except Exception as e:
                print(f'Erro ao converter leitura para inteiro: {e}')

            self.watcher.save_frame(image, 'result.jpg')

    def send_message(self, image64, weight):
        """Envia a imagem e o peso para a API do WhatsApp"""
        message = f'⚠ALERTA DE EXCESSO DE PESO NO GUINCHO\n🕒Horário: { datetime.now().strftime("%d/%m/%Y, %H:%M:%S") }\n🏗Peso detectado: { weight }kg\n🔴Situação: Valor lido excede o limite de 3.000 kg.\n📍Local: Área de Carga - Subsolo Extração 2 - Acesso B1\n👥Notificação enviada ao corpo técnico e supervisão\n❕Confirme o peso na imagem em anexo.'
        try:
            requests.post(self.api_url, json = { 'image': image64, 'weight': weight, 'message': message, 'pid': self.process_id }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

if __name__ == "__main__":
    monitoring = Monitoring(STREAM_URL, API_URL)
    monitoring.start()
