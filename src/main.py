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

        self.save_result_frame = True
        self.save_overlap_frames = True

        self.max_weight_detected = 0
        self.max_weight_detected_image = None

        self.process_id = os.getpid()
        self.api_url = api_url

    def start(self):
        """Inicia o monitoramento da stream"""
        try:
            self.send_message(self.__message_start())
            self.__main_loop()
        except KeyboardInterrupt:
            self.send_message(self.__message_stop(), self.max_weight_detected_image)
        finally:
            self.watcher.stop()

    def __main_loop(self):
        while True:
            start_time = time.time()

            frame = self.watcher.get_frame()
            [result, image] = self.reader.get_frame_text(frame)

            self.check_and_send_message(result, image, start_time)

            if self.save_result_frame:
                self.watcher.save_frame(image, 'result.jpg')
            
            if self.save_overlap_frames:
                self.watcher.save_frame(self.reader.last_overlap_frame, 'overlap.jpg')
                self.reader.last_overlap_frame = None

            time.sleep(self.loop_delay)

    def check_and_send_message(self, result, image, start_time):
        reading_time = time.time() - start_time
        timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        try:
            weight_detected = int(result)
            if weight_detected > self.max_weight_detected:
                self.max_weight_detected = weight_detected
                self.max_weight_detected_image = image

            if self.weight_trigger <= weight_detected <= self.valid_max_weight:
                if start_time - self.last_message_time >= self.message_delay:
                    self.send_weight_alert_message(image, result, timestamp)
                    print(f'Peso detectado: {result}kg - Mensagem enviada (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')
                else:
                    print(f'Peso detectado: {result}kg - Mensagem já enviada anteriormente (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')
            else:
                self.weight_exceeded = False
                print(f'Peso detectado: {result}kg - Dentro do limite (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

        except Exception as e:
            print(f'Erro ao converter leitura para inteiro: {e} (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

    def send_weight_alert_message(self, image, weight, timestamp):
        """Envia uma mensagem personalizada para a API do WhatsApp"""
        message = self.__message_weight(timestamp, weight)
        self.send_message(message, image, weight)
        self.last_message_time = time.time()

    def send_message(self, message, image=None, weight=None):
        """Envia uma mensagem para a API do WhatsApp"""
        image64 = None if image is None else self.watcher.ndarray_to_base64(image)
        try:
            requests.post(self.api_url, json = { 'image': image64, 'weight': weight, 'message': message, 'pid': self.process_id }, timeout = 300)
        except requests.RequestException as e:
            print(f'Erro ao enviar mensagem: {e}')

    def __message_start(self):
        return "Iniciando monitoramento de peso no guincho."
    
    def __message_stop(self):
        return f'''Encerrando monitoramento de peso no guincho.
⚠ Peso máximo detectado: {self.max_weight_detected}kg
🔎 Confirme o peso na imagem em anexo'''

    def __message_weight(self, timestamp, detected_weight):
        return f'''⚠ POSSÍVEL EXCESSO DE PESO NO GUINCHO
🔎 Confirme o peso na imagem em anexo
🕒 Horário: {timestamp}
🔴 Situação: Valor pode exceder o limite de {self.weight_trigger}kg
📍 Local: Área de Carga - *Elevador Principal* - Extração 2 - Acesso B1
👥 Notificação enviada a Central de monitoramento, Corpo técnico e Supervisores'''

if __name__ == "__main__":
    monitoring = Monitoring(STREAM_URL, API_URL)
    monitoring.start()
