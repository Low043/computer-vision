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

        self.weight_trigger = 3000
        self.valid_max_weight = 4000
        self.last_message_time = 0

        self.loop_delay = 1
        self.message_delay = 3

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
            start_time = time.time()

            frame = self.watcher.get_frame()
            [result, image] = self.reader.get_frame_text(frame)

            self.check_and_send_message(result, image, start_time)
            self.watcher.save_frame(image, 'result.jpg')

            time.sleep(self.loop_delay)

    def check_and_send_message(self, result, image, start_time):
        reading_time = time.time() - start_time
        timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        try:
            weight_detected = int(result)
            if self.weight_trigger <= weight_detected <= self.valid_max_weight:
                if start_time - self.last_message_time >= self.message_delay:
                    self.send_message(image, result, timestamp)
                    print(f'Peso detectado: {result}kg - Mensagem enviada (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')
                else:
                    print(f'Peso detectado: {result}kg - Mensagem já enviada anteriormente (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')
            else:
                self.weight_exceeded = False
                print(f'Peso detectado: {result}kg - Dentro do limite (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

        except Exception as e:
            print(f'Erro ao converter leitura para inteiro: {e} (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

    def send_message(self, image, weight, timestamp):
        """Envia a imagem e o peso para a API do WhatsApp"""
        image64 = self.watcher.ndarray_to_base64(image)
        message = f'⚠ALERTA DE EXCESSO DE PESO NO GUINCHO\n🕒Horário: {timestamp}\n🏗Peso detectado: {weight}kg\n🔴Situação: Valor lido excede o limite de {self.weight_trigger}kg.\n📍Local: Área de Carga - Subsolo Extração 2 - Acesso B1\n👥Notificação enviada ao corpo técnico e supervisão\n❕Confirme o peso na imagem em anexo.'
        try:
            requests.post(self.api_url, json = { 'image': image64, 'weight': weight, 'message': message, 'pid': self.process_id }, timeout = 300)
            self.last_message_time = time.time()
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

if __name__ == "__main__":
    monitoring = Monitoring(STREAM_URL, API_URL)
    monitoring.start()
