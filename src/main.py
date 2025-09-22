"""Orquestra a execução do app"""
from services.messager import Messager
from services.watcher import Watcher
from services.reader import Reader
from datetime import datetime
import dotenv
import time

STREAM_URL = dotenv.get_key(dotenv.find_dotenv(), 'STREAM_URL')
API_URL = dotenv.get_key(dotenv.find_dotenv(), 'API_URL')

class Monitoring:
    """Classe responsável pela lógica do monitoramento da stream"""
    def __init__(self, stream_url, api_url):
        self.messager = Messager(api_url)
        self.watcher = Watcher(stream_url).start()
        self.reader = Reader()

        self.weight_trigger = 2300
        self.valid_max_weight = 4000
        self.last_message_time = 0

        self.loop_delay = 1
        self.message_delay = 45

        self.save_result_frame = True
        self.save_overlap_frames = True

        self.max_weight_detected = 0
        self.max_weight_detected_image = None

    def start(self):
        """Inicia o monitoramento da stream"""
        try:
            self.messager.send_start_message()
            self.__main_loop()
        except KeyboardInterrupt:
            self.messager.send_stop_message(self.max_weight_detected_image, self.max_weight_detected)
        finally:
            self.watcher.stop()

    def __main_loop(self):
        while True:
            start_time = time.time()

            frame = self.watcher.get_frame()
            [result, image] = self.reader.get_frame_text(frame)

            self.check_weight(result, image, start_time)

            if self.save_result_frame:
                self.watcher.save_frame(image, 'result.jpg')

            if self.save_overlap_frames:
                self.watcher.save_frame(self.reader.last_overlap_frame, 'overlap.jpg')
                self.reader.last_overlap_frame = None

            time.sleep(self.loop_delay)

    def check_weight(self, result, image, start_time):
        """Verifica se o peso excedeu o limite"""
        reading_time = time.time() - start_time
        timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        time_since_last_message = start_time - self.last_message_time

        try:
            weight_detected = int(result)

            if weight_detected > self.valid_max_weight:
                self.logger('weight_invalid', result, reading_time, timestamp)
                return
            if weight_detected > self.max_weight_detected:
                self.max_weight_detected = weight_detected
                self.max_weight_detected_image = image
            if weight_detected < self.weight_trigger:
                self.logger('weight_valid', result, reading_time, timestamp)
                return
            if time_since_last_message < self.message_delay:
                self.logger('alert_already_sended', result, reading_time, timestamp)
                return

            self.messager.send_weight_exceeded_message(self.weight_trigger, weight_detected, image, timestamp)
            self.last_message_time = time.time()
            self.logger('alert', result, reading_time, timestamp)

        except Exception as e:
            self.logger('error', e, reading_time, timestamp)

    def logger(self, type, result = None, reading_time = None, timestamp = None):
        """Registra o resultado da leitura no arquivo de log"""
        match type:
            case 'alert':
                print(f'Peso detectado: {result}kg - Mensagem enviada (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

            case 'alert_already_sended':
                print(f'Peso detectado: {result}kg - Mensagem já enviada anteriormente (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

            case 'weight_valid':
                print(f'Peso detectado: {result}kg - Dentro do limite (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

            case 'weight_invalid':
                print(f'Peso detectado: {result}kg - Invalido (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')

            case 'error':
                print(f'Erro ao converter leitura para inteiro: {result} (Reading Time: {reading_time:.2f}s) (Timestamp: {timestamp})')


if __name__ == "__main__":
    monitoring = Monitoring(STREAM_URL, API_URL)
    monitoring.start()
